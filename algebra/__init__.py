"""
Algebra module for advanced algebraic computations.

This module provides advanced algebraic operations including:
- Lattice operations and enumeration
- LLL (Lenstra-Lenstra-Lovász) lattice reduction
- Gram-Schmidt orthogonalization
- Finite field constructions
- Vector and matrix norms
- Lattice enumeration algorithms

Key Functions:
    lll_reduction: LLL lattice reduction algorithm
    gram_schmidt_numpy: Gram-Schmidt orthogonalization process
    euclidean_norm: Euclidean vector norm
    weighted_frobenius_norm: Weighted Frobenius matrix norm
"""

# Import key functions for the public API
try:
    from .lll import lll_reduction
    from .norms import euclidean_norm, weighted_frobenius_norm, sum_of_squared_coefficietns
    
    __all__ = [
        'lll_reduction', 'euclidean_norm', 'weighted_frobenius_norm', 
        'sum_of_squared_coefficietns'
    ]
except ImportError as e:
    # Handle missing dependencies gracefully
    print(f"Warning: Some algebra functions not available: {e}")
    __all__ = []