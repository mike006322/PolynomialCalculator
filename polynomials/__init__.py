"""
Polynomials module for polynomial arithmetic and operations.

This module provides comprehensive polynomial operations including:
- Polynomial construction from strings or matrices
- Arithmetic operations (addition, multiplication, division)
- Ideal theory and Gröbner basis computations
- Polynomial parsing and formatting
- Term ordering and manipulation

Key Classes:
    Polynomial: Main polynomial class with arithmetic operations
    Ideal: Polynomial ideal operations and Gröbner basis computation
    NonFactor: Exception for non-divisible polynomial operations

Functions:
    division_algorithm: Multivariate polynomial division
    gcd: Greatest common divisor of polynomials
    lcm: Least common multiple of polynomials
"""

from .polynomial import Polynomial, NonFactor, division_algorithm, gcd, lcm
from .ideal import Ideal
from .formulas import solve
from .orderings import order_lex, graded_lex, order_grevlex
from .collect_like_terms import collect_like_terms

__all__ = [
    'Polynomial', 'NonFactor', 'Ideal',
    'division_algorithm', 'gcd', 'lcm', 'solve',
    'order_lex', 'graded_lex', 'order_grevlex', 
    'collect_like_terms'
]