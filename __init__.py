"""
PolynomialCalculator - A comprehensive polynomial computation library.

This package provides tools for polynomial arithmetic, algebraic computations,
and mathematical operations including:
- Polynomial operations and representations
- Ideal theory and Gröbner bases
- Linear algebra operations
- Lattice computations
- Various mathematical utilities

Modules:
    polynomials: Core polynomial operations and representations
    algebra: Advanced algebraic computations and lattice operations
    utils: Utility functions and data structures
"""

__version__ = "0.2.0"
__author__ = "mike006322"

# Import main classes for convenience
from polynomials.polynomial import Polynomial
from polynomials.ideal import Ideal

__all__ = ['Polynomial', 'Ideal']