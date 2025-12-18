import math
import cmath
from decimal import Decimal, getcontext, ROUND_HALF_EVEN

# ============================================================
# GLOBAL SETTINGS
# ============================================================

getcontext().prec = 120
ROUNDING = ROUND_HALF_EVEN
FORCE_POSITIONAL = True
MAX_COMPLEX_DIGITS = 200

HEX_MAP = "0123456789ABCDEF"
OMEGA = complex(-0.5, math.sqrt(3) / 2)

# ============================================================
# BASE LABELS
# ============================================================

def base_label(b):
    if abs(b - math.pi) < 1e-12:
        return "π"
    if abs(b - math.sqrt(2)) < 1e-12:
        return "√2"
    if abs(b - ((1 + math.sqrt(5)) / 2)) < 1e-12:
        return "φ"
    if b == -1 + 1j:
        return "-1+i"
    if b == -1 + OMEGA:
        return "-1+ω"
    return str(b)

# ============================================================
# PARSING
# ============================================================

def parse_complex(s):
    return complex(s.replace("i", "j").replace("ω", "j"))

def parse_integer_digits(s):
    if not s.isdigit():
        raise ValueError("Invalid integer input for positional base.")
    return [int(c) for c in s]

# ============================================================
# RECONSTRUCTION
# ============================================================

def reconstruct(I, F, base):
    v = 0 + 0j
    for i, d in enumerate(reversed(I)):
        v += d * base**i
    for i, d in enumerate(F, start=1):
        v += d * base**(-i)
    return v

# ============================================================
# POSITIVE-MAGNITUDE BASE CONVERSION (|base| > 1)
# ============================================================

def beta_expand(value, base, frac_digits):
    remainder = value
    I, F = [], []

    k = int(math.floor(math.log(abs(value), abs(base)))) if value != 0 else 0

    for p in range(k, -1, -1):
        d = int(round((remainder / base**p).real))
        I.append(d)
        remainder -= d * base**p

    for _ in range(frac_digits):
        remainder *= base
        d = int(round(remainder.real))
        F.append(d)
        remainder -= d

    approx = reconstruct(I, F, base)
    actual_error = abs(value - approx)

    bound = 0.0 if actual_error == 0 else abs(base) ** (-frac_digits)
    return I, F, approx, actual_error, bound

# ============================================================
# GAUSSIAN BASE (−1+i)
# ============================================================

def gaussian_convert(z, balanced=True):
    beta = -1 + 1j
    digits = []
    z = complex(round(z.real), round(z.imag))

    while z != 0 and len(digits) < MAX_COMPLEX_DIGITS:
        if balanced:
            r = int(round((z.real + z.imag) % 2))
            if r == 2:
                r = -1
        else:
            r = int((z.real + z.imag) % 2)

        digits.append(r)
        z = (z - r) / beta
        z = complex(round(z.real), round(z.imag))

    return digits[::-1]

# ============================================================
# EISENSTEIN BASE (−1+ω)
# ============================================================

def eisenstein_convert(z):
    beta = -1 + OMEGA
    digits = []
    z = complex(round(z.real), round(z.imag))

    while z != 0 and len(digits) < MAX_COMPLEX_DIGITS:
        r = int(round(z.real)) % 3 - 1
        digits.append(r)
        z = (z - r) / beta
        z = complex(round(z.real), round(z.imag))

    return digits[::-1]

# ============================================================
# FORMATTING
# ============================================================

def format_hex(I):
    return "".join(HEX_MAP[d] for d in I) + "_16"

def format_universal(I, F, base):
    i = ", ".join(str(d) for d in I)
    if not F or all(d == 0 for d in F):
        return f"⟨{i} |⟩_{base_label(base)}"
    f = ", ".join(str(d) for d in F)
    return f"⟨{i} | {f}⟩_{base_label(base)}"

# ============================================================
# CLI
# ============================================================

def run_cli():
    print("=" * 76)
    print("UNIVERSAL BASE CONVERTER — RECIPROCAL-SAFE FINAL EDITION")
    print("=" * 76)

    num = input("Enter number: ").strip()
    src_base = parse_complex(input("Enter source base: ").strip())
    dst_base = parse_complex(input("Enter target base: ").strip())

    frac_digits = int(input("Fractional digits: "))
    mode = input("Gaussian mode [balanced/unbalanced/none/eisenstein]: ").strip().lower()

    # Source parsing
    if src_base.imag == 0 and src_base.real == int(src_base.real):
        digits = parse_integer_digits(num)
        value = reconstruct(digits, [], int(src_base.real))
    else:
        value = parse_complex(num)

    reciprocal_used = False

    # =====================================================
    # BASE VALIDATION & RECIPROCAL HANDLING
    # =====================================================

    if abs(dst_base) == 1:
        raise ValueError("Invalid base: |base| = 1 does not define a numeral system.")

    if abs(dst_base) < 1:
        reciprocal_used = True
        original_base = dst_base
        dst_base = 1 / dst_base

    # =====================================================
    # CONVERSION
    # =====================================================

    if dst_base == -1 + 1j:
        I = gaussian_convert(value, balanced=(mode != "unbalanced"))
        F = []
        approx = reconstruct(I, F, dst_base)
        actual_error = abs(value - approx)
        bound = 0.0

    elif mode == "eisenstein":
        I = eisenstein_convert(value)
        F = []
        approx = reconstruct(I, F, dst_base)
        actual_error = abs(value - approx)
        bound = 0.0

    else:
        I, F, approx, actual_error, bound = beta_expand(value, dst_base, frac_digits)

        if FORCE_POSITIONAL and dst_base.imag == 0 and dst_base.real > 10 and len(I) == 1:
            I = [0] + I

    # =====================================================
    # OUTPUT
    # =====================================================

    print("=" * 76)
    print("Parsed value        :", value)

    if reciprocal_used:
        print("NOTE:")
        print(f"  |base| < 1 detected. Using reciprocal base γ = 1/β = {dst_base}")
        print(f"  Digits represent powers of γ⁻¹ (stable positional system).")

    if dst_base == 16:
        print("Representation     :", format_hex(I))
    else:
        print("Representation     :", format_universal(I, F, dst_base))

    print("Reconstructed      :", approx)
    print("Actual error       :", actual_error)
    print("Error bound ≤      :", bound)
    print("Verified           :", actual_error <= bound + 1e-12)
    print("=" * 76)

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_cli()
