#!/usr/bin/env python3
"""
PolynomialCalculator Demo Script
A comprehensive demonstration of polynomial operations, algebra, and finite fields.

This script showcases the capabilities of PolynomialCalculator v0.2.0.
Run with: python demo.py
"""

from polynomials import Polynomial, Ideal, gcd, lcm, division_algorithm
from polynomials.display import format_number
import sys


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)

# Helpers to format numeric outputs consistently

def _strip_trailing_dot_zero(s: str) -> str:
    """Remove trailing .0 from numeric strings (e.g., '2.0' -> '2')."""
    return s[:-2] if s.endswith('.0') else s


def _fmt_val(x):
    """Format a single value using the global numeric formatter, avoiding '.0' for integers."""
    try:
        s = format_number(x)
        return _strip_trailing_dot_zero(s)
    except Exception:
        # Best-effort fallback
        try:
            import math
            if isinstance(x, float) and x.is_integer():
                return str(int(x))
        except Exception:
            pass
        return str(x)


def _fmt_seq(seq):
    """Format a sequence of values using the global numeric formatter, avoiding '.0' for integers."""
    try:
        return "[ " + ", ".join(_fmt_val(s) for s in seq) + " ]"
    except Exception:
        return str(seq)


def basic_polynomial_operations():
    """Demonstrate basic polynomial arithmetic."""
    print_section("Basic Polynomial Operations")
    
    # Create polynomials using string expressions
    f = Polynomial('x + 1')
    g = Polynomial('x - 1') 
    h = Polynomial('x^2 + 2*x + 1')
    
    print(f"f = {f}")
    print(f"g = {g}")
    print(f"h = {h}")
    print()
    
    # Arithmetic operations
    print("Polynomial Arithmetic:")
    print(f"f * g = {f * g}")
    print(f"f + g = {f + g}")
    print(f"h / f = {h / f}")
    print(f"h % f = {h % f}")
    print()
    
    # Solve equations
    print("Solutions:")
    print(f"Solutions to f*g = 0: {_fmt_seq((f * g).solve())}")
    print(f"Solutions to h = 0: {_fmt_seq(h.solve())}")


def gcd_lcm_operations():
    """Demonstrate GCD and LCM operations."""
    print_section("GCD & LCM Operations")
    
    # Polynomials with common factors
    a = Polynomial('x^3 - x')           # x(x^2 - 1) = x(x-1)(x+1)
    b = Polynomial('x^2 - 1')           # (x-1)(x+1)
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"gcd(a, b) = {gcd(a, b)}")
    print(f"lcm(a, b) = {lcm(a, b)}")
    print()
    
    # Verify: a * b = gcd(a,b) * lcm(a,b)
    product_ab = a * b
    product_gcd_lcm = gcd(a, b) * lcm(a, b)
    print(f"Verification: a * b = {product_ab}")
    print(f"gcd * lcm = {product_gcd_lcm}")
    print(f"Equal? {product_ab == product_gcd_lcm}")


def multivariate_polynomials():
    """Demonstrate multivariate polynomial operations."""
    print_section("Multivariate Polynomials")
    
    poly = Polynomial('x^2*y + x*y^2 + 3*x + 2*y - 1')
    print(f"p(x,y) = {poly}")
    print(f"Variables: {poly.variables}")
    print(f"Degree: {poly.degree()}")
    print(f"Number of variables: {poly.number_of_variables}")
    print()
    
    # Partial derivatives
    print("Partial Derivatives:")
    print(f"∂p/∂x = {poly.derivative('x')}")
    print(f"∂p/∂y = {poly.derivative('y')}")
    print()
    
    # Evaluation
    print("Evaluation:")
    print(f"p(1, 2) = {_fmt_val(poly(1, 2))}")
    print(f"p(0, 0) = {_fmt_val(poly(0, 0))}")


def groebner_basis_demo():
    """Demonstrate Gröbner basis computation."""
    print_section("Gröbner Basis Computation")
    
    # Classic example: circle and line intersection
    f1 = Polynomial('x^2 + y^2 - 1')  # Unit circle
    f2 = Polynomial('x - y')          # Line y = x
    
    print("Finding intersection of unit circle and line y = x:")
    print(f"f1 = {f1}  (unit circle)")
    print(f"f2 = {f2}  (line y = x)")
    print()
    
    I = Ideal(f1, f2)
    gb = I.groebner_basis()
    print("Gröbner basis:")
    for i, poly in enumerate(gb, 1):
        print(f"  G{i} = {poly}")
    print()
    
    # Another example: more complex system
    print("More complex system:")
    p1 = Polynomial('x^2*y - 1')
    p2 = Polynomial('x*y^2 - x')
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    
    J = Ideal(p1, p2)
    gb2 = J.groebner_basis()
    print("Gröbner basis:")
    for i, poly in enumerate(gb2, 1):
        print(f"  H{i} = {poly}")


def order_independent_equality():
    """Demonstrate order-independent polynomial equality."""
    print_section("Order-Independent Equality")
    
    # Same polynomial, different term orders
    p1 = Polynomial('x^2 + 2*x + 1')
    p2 = Polynomial('1 + 2*x + x^2')
    p3 = Polynomial('2*x + x^2 + 1')
    
    print("Testing order-independent equality:")
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p3 = {p3}")
    print()
    print(f"p1 == p2: {p1 == p2}")
    print(f"p1 == p3: {p1 == p3}")
    print(f"p2 == p3: {p2 == p3}")
    print()
    
    # Different polynomials
    p4 = Polynomial('x^2 + 2*x + 2')
    print(f"p4 = {p4}")
    print(f"p1 == p4: {p1 == p4}")


def finite_field_operations():
    """Demonstrate finite field operations."""
    print_section("Finite Field Operations")
    
    try:
        from algebra.construct_finite_field import ZechLogarithmTable, random_monic, find_irreducible
        
        # Polynomials over F_2
        print("Polynomials over F_2 (binary field):")
        f = Polynomial('x^3 + x + 1', 2)  
        g = Polynomial('x^2 + 1', 2)      
        
        print(f"f = {f} (over F_2)")
        print(f"g = {g} (over F_2)")
        print(f"f + g = {f + g}")
        print(f"f * g = {f * g}")
        print(f"gcd(f, g) = {gcd(f, g)}")
        print()
        
        # Finite field construction
        print("Finite Field GF(2^3):")
        field = ZechLogarithmTable(2, 3)
        print(f"Irreducible polynomial: {field.h}")
        print(f"Field size: {_fmt_val(len(field.poly_to_power))} elements")
        print()
        
        # Random polynomial generation
        print("Random polynomial generation:")
        random_poly = random_monic(3, 4)
        print(f"Random monic polynomial over F_3 of degree 4: {random_poly}")
        
        # Find irreducible polynomial
        irreducible = find_irreducible(2, 3)
        print(f"Irreducible polynomial over F_2 of degree 3: {irreducible}")
        
    except ImportError:
        print("Finite field operations require optional dependencies (numpy, scipy)")
        print("Install with: pip install PolynomialCalculator[algebra]")


def polynomial_calculus():
    """Demonstrate polynomial calculus operations."""
    print_section("Polynomial Calculus")
    
    # Use a simpler polynomial for demonstration
    poly = Polynomial('x^3 - 3*x^2 + 2*x')
    print(f"f(x) = {poly}")
    print()
    
    # Derivatives
    first_deriv = poly.derivative('x')
    second_deriv = first_deriv.derivative('x')
    
    print("Derivatives:")
    print(f"f'(x) = {first_deriv}")
    print(f"f''(x) = {second_deriv}")
    print()
    
    # Critical points (where f'(x) = 0)
    print("Finding critical points:")
    try:
        critical_points = first_deriv.solve()
        print(f"Solutions to f'(x) = 0: {_fmt_seq(critical_points)}")
    except Exception as e:
        print(f"Critical point solving requires numerical methods for this polynomial")
        print(f"f'(x) = {first_deriv} (degree {_fmt_val(first_deriv.degree())})")
    print()
    
    # Evaluation at specific points
    print("Function evaluation:")
    for x_val in [0, 1, 2]:
        y_val = poly(x_val)
        print(f"f({x_val}) = {_fmt_val(y_val)}")
    
    # Factor the polynomial if possible
    print(f"\nFactorization:")
    print(f"f(x) = x(x^2 - 3*x + 2) = x(x - 1)(x - 2)")
    print(f"Roots: x = 0, 1, 2")


def advanced_examples():
    """Show advanced polynomial system solving."""
    print_section("Advanced Examples")
    
    print("System: Circle and parabola intersection")
    print("x^2 + y^2 = 4  (circle of radius 2)")
    print("y = x^2 - 1   (parabola)")
    print()
    
    circle = Polynomial('x^2 + y^2 - 4')
    parabola = Polynomial('y - x^2 + 1')
    
    print(f"Circle: {circle}")
    print(f"Parabola: {parabola}")
    
    system = Ideal(circle, parabola)
    gb = system.groebner_basis()
    
    print("Gröbner basis for the system:")
    for i, poly in enumerate(gb, 1):
        print(f"  {poly}")
    print()
    
    # Try to solve the system
    try:
        solutions = system.solve_system_structured()
        if solutions is None:
            print("System has infinite/undetermined solutions - use Gröbner basis for analysis")
        elif len(solutions) and len(str(solutions)) < 200:
            print("System solutions (structured):")
            for sol in solutions:
                ordered = ", ".join(f"{k} = {_fmt_val(sol[k])}" for k in sorted(sol.keys()))
                print(f"  [ {ordered} ]")
        else:
            print("System has complex solutions - use Gröbner basis for analysis")
    except Exception as e:
        print(f"System solving encountered: {type(e).__name__}")
        print("This demonstrates the complexity of general polynomial systems!")


def main():
    """Run all demonstrations."""
    print("PolynomialCalculator v0.2.0 - Comprehensive Demo")
    print("=" * 50)
    print("Showcasing polynomial operations, algebra, and finite fields")
    
    try:
        basic_polynomial_operations()
        gcd_lcm_operations()
        multivariate_polynomials()
        polynomial_calculus()
        order_independent_equality()
        groebner_basis_demo()
        advanced_examples()
        finite_field_operations()
        
        print_section("Demo Complete")
        print("✅ All demonstrations completed successfully!")
        print("\nFor interactive exploration, try:")
        print("- python -c \"from polynomials import *; help(Polynomial)\"")
        print("- jupyter notebook PolyCalc_demo.ipynb")
        print("- polycalc --help  # (after installation)")
        
    except Exception as e:
        print(f"\n❌ Demo encountered error: {e}")
        print(f"Error type: {type(e).__name__}")
        sys.exit(1)


if __name__ == '__main__':
    main()
