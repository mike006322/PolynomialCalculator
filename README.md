<img src = "https://github.com/mike006322/PolynomialCalculator/blob/master/logo.svg" height = 200>

# Polynomial Calculator
[![CI](https://github.com/mike006322/PolynomialCalculator/actions/workflows/ci.yml/badge.svg)](https://github.com/mike006322/PolynomialCalculator/actions/workflows/ci.yml)
*A lightweight Computer Algebra System for polynomial computations over finite fields*


### Features

- Polynomial operations: +, -, *, /, %, gcd
- Supports polynomials over field of characteristic > 0 (A field of characteristic $$p > 0$$ is one where arithmetic behaves like modulo $$p$$, meaning $$p$$ copies of 1 add up to 0).
- Supports multi-variable polynomials
- Numerical solutions for single-variable polynomials
- Numerical solutions for systems of polynomials
- Support for constructing finite fields with polynomials
- Can find Gröbner basis for polynomial Ideals

### Command Line Interface

PolynomialCalculator provides a powerful command-line interface with the following commands:

- `finite_field`: Create finite fields and display Zech logarithm information  
- `random_monic`: Generate random monic polynomials over finite fields
- `find_irreducible`: Find irreducible polynomials of specified degree
- `gcd`: Compute greatest common divisor of polynomials  
- `solve`: Solve univariate polynomial equations over rationals
- `groebner`: Compute Gröbner basis for polynomial ideals

Global options:
- `--numeric-output {float,rational}` to control numeric display (default: `float`)
- Convenience flags: `--float`, `--rational`
- Logging: `--verbose` for debug logs, `--quiet` to show errors only
- Machine-readable: `--json` to emit JSON for `solve` and `solve-system`
  (also supported for `groebner`)

Use `polycalc --help` or `polycalc <command> --help` for detailed usage information.

**Alternative Usage**: If you haven't installed the package, you can substitute:
- `python polycalc.py` (using the wrapper script)  
- `python -m polynomials.cli` (running as a module)

### Usage Examples




#### Create a finite field GF(2^3):
```bash
polycalc finite_field -p 2 3
```
```
Created GF(2^3) with irreducible polynomial: x^3 + x + 1
Primitive element table size: 7 elements
```

#### Generate a random monic polynomial of degree 4 over F_5:
```bash
polycalc random_monic -p 5 4
```
```
Random monic polynomial over F_5 of degree 4: x^4 + 3x^3 + x^2 + 2x + 2
```

#### Find an irreducible polynomial of degree 3 over F_3:
```bash
polycalc find_irreducible -p 3 3
```
```
Irreducible polynomial over F_3 of degree 3: x^3 + 2x^2 + x + 1
```

#### Compute the GCD of two polynomials over F_2:
```bash
polycalc gcd "x^3+x+1" "x^2+1" -p 2
```
```
gcd(x^3 + x + 1, x^2 + 1) = 1
```

#### Solve a univariate polynomial equation:
```bash
polycalc solve "x^2-2" x
```
```
Solutions to x^2-2 = 0:
  1.4142135623730951
  -1.4142135623730951
```

#### Compute a Groebner basis for a system of polynomials:
```bash
polycalc groebner "x^2+y^2-1" "x-y"
```
```
Groebner basis:
  x - y
  2y^2 - 1
```

You can choose the monomial order with `--order {lex,grlex,grevlex}`:
```bash
polycalc groebner "x^2+y^2-1" "x-y" --order grevlex
```

#### Control numeric output formatting
Default is float mode. Use `--rational` to prefer exact-looking output when possible.

Environment variable:
- Set `POLYCALC_NUMERIC_OUTPUT` to `float` or `rational` to control the default mode.

```bash
polycalc --rational solve-system "x-1" "y-2"
```
```
1 solutions:
  [ x = 1, y = 2 ]
```

```bash
polycalc --float solve-system "x-1" "y-2"
```
```
1 solutions:
  [ x = 1.0, y = 2.0 ]
```

#### JSON output
Add `--json` to `solve`, `solve-system`, or `groebner` for structured output.

Examples:
```bash
polycalc --json solve "x^2-2" x
```
Outputs:
```json
{ "command": "solve", "poly": "x^2-2", "var": "x", "solutions": [1.4142135623730951, -1.4142135623730951], "count": 2, "status": "ok" }
```

```bash
polycalc --json solve-system "x-1" "y-2"
```
Outputs:
```json
{ "command": "solve-system", "polys": ["x-1", "y-2"], "status": "ok", "solutions": [{"x": 1.0, "y": 2.0}], "count": 1 }
```

On errors, JSON mode returns:
```json
{ "status": "error", "error": "<message>" }
```

Groebner example:
```bash
polycalc --json groebner "x^2+y^2-1" "x-y" --order grevlex
```
Outputs:
```json
{ "command": "groebner", "polys": ["x^2+y^2-1","x-y"], "order": "grevlex", "status": "ok", "basis": ["x - y", "2y^2 - 1"], "count": 2 }
```

### Logging and diagnostics

- CLI logging:
  - `--verbose` enables debug-level logs from internal modules.
  - `--quiet` suppresses non-error output (only errors are shown).
- Core debug tracing:
  - Set environment variable `POLYCALC_DEBUG=1` to enable additional debug traces in some core algorithms (e.g., division algorithm and gcd).
  - This is off by default and only emits when combined with a suitable logging level.

### Near-term goals:
- implement faster gcd algorithm
- implement lookup tables for primitive field elements
- implement 'factor' algorithm to factor over polynomials over finite fields
- option to plot single-variable polynomials
- create a GUI with Python

### Longer-term goals
- web GUI
- Mobile app

### Installation

#### Option 1: Install as a package (Recommended)
```bash
git clone https://github.com/mike006322/PolynomialCalculator.git
cd PolynomialCalculator
pip install -e .
```
After installation, you can use the `polycalc` command directly:
```bash
polycalc solve "x^2-2" x
```

#### Option 2: Use the wrapper script
If you prefer not to install the package, you can use the provided wrapper script:
```bash
git clone https://github.com/mike006322/PolynomialCalculator.git
cd PolynomialCalculator
python polycalc.py solve "x^2-2" x
```

#### Option 3: Run as a Python module
#### Optional features (algebra extras)
Some features depend on optional scientific libraries. Install with extras:
```bash
pip install "PolynomialCalculator[algebra]"
```
This pulls in numpy and scipy for algebra/finite field operations.
```bash
python -m polynomials.cli solve "x^2-2" x
```

### Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

Please make sure to update tests as appropriate.

Developer tooling:
- Lint/format: ruff and black (configured via pyproject.toml)
- Pre-commit hooks: install with `pip install pre-commit` then `pre-commit install`
- CI: GitHub Actions runs tests on Python 3.10–3.12 across Windows/Linux/macOS


### Similar projects:
- [SAGE](http://doc.sagemath.org/)

- [Sympy](https://github.com/sympy/sympy)


- [CoCa](http://cocoa.dima.unige.it/) written in C++ and CoCa language

- jasymchat - Computer Algebra System written in Java (won't run on phone, seems defunct)
