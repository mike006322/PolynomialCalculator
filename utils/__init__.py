"""
Utilities module for common data structures and algorithms.

This module provides utility functions and data structures used throughout
the polynomial calculator:
- Depth-first search algorithms
- Tree traversal operations
- Common algorithmic utilities

Key Functions:
    dfs_pre_order: Pre-order depth-first search
    dfs_post_order: Post-order depth-first search
"""

from .dfs import dfs_pre_order, dfs_post_order

__all__ = ['dfs_pre_order', 'dfs_post_order']