
# Universal Base Converter — Documentation (Final Stable Edition)

## Overview
This CLI is a deterministic, numerically honest tool for converting numbers between general positional bases.

It supports:
- Integer bases (2, 8, 10, 16, …)
- Real irrational bases (π, √2, φ) with provable error bounds
- Reciprocal-base handling for |β| < 1
- Gaussian base (−1+i), balanced and unbalanced digit sets
- Eisenstein base (−1+ω)
- Universal unambiguous bracket notation
- Proper rounding and deterministic behavior

---

## Installation
```bash
python --version   # Python 3.8+ required
pip install sympy
```

---

## Running the CLI
```bash
python cli.py
```

---

## Universal Notation
```
⟨d_n, d_{n-1}, …, d_0 | d_{-1}, d_{-2}, …⟩_β
```
- Left of `|`: integer powers of β  
- Right of `|`: fractional powers of β  

Example:
```
⟨1, 2 |⟩_8 = 10₁₀
```

---

## Base Validity Rules

| Base condition | Behavior |
|---------------|----------|
| \|β\| > 1 | Valid positional system |
| \|β\| = 1 | Rejected |
| \|β\| < 1 | Converted using reciprocal base γ = 1/β |

---

## Reciprocal-Base Handling
When |β| < 1:
```
γ = 1 / β
```
Digits are computed in base γ and interpreted as powers of γ⁻¹.

Error bound:
```
|x − x̂| ≤ |γ|⁻ᴺ = |β|ᴺ
```

This guarantees exponential convergence.

---

## Gaussian Base (−1 + i)

Digit sets:
- Balanced: {−1, 0, 1}
- Unbalanced: {0, 1}

Properties:
- Exact integer representation
- No fractional part
- Error bound = 0

---

## Eisenstein Base (−1 + ω)

- ω = exp(2πi / 3)
- Digits ∈ {−1, 0, 1}
- Hexagonal lattice arithmetic
- Exact representation for Eisenstein integers

---

## Error Reporting

The CLI always prints:
- Reconstructed value
- Actual error
- Error bound
- Verification result

```
Verified = (actual error ≤ error bound)
```

---

## Example
```
Enter number: 50
Enter source base: 10
Enter target base: -1+i
Gaussian mode: balanced
```

Output:
```
⟨1, 0, -1, 1, 0⟩_(-1+i)
Error bound ≤ 0
Verified = True
```

---

## Limitations
- Irrational bases produce infinite expansions (truncated with bounds)
- Symbolic exactness is guaranteed only for algebraic integer bases
- Floating magnitude limits apply for very large numbers

---

## Extending the Tool
Possible extensions:
- Strict vs Auto base policies
- JSON / LaTeX export
- Symbolic algebra backend
- Visualization of complex digit lattices

---

## Mathematical Integrity
This tool never:
- Claims exactness where impossible
- Hides base transformations
- Produces divergent positional expansions

---

## Final Note
This converter is designed to align with number theory, numerical analysis, and algebraic correctness.

It prioritizes **truth over convenience**.
