"""
Display utilities for controlling numeric formatting across PolynomialCalculator.

Default mode is 'float' to preserve existing behaviors/tests.
'rational' mode prefers exact-looking output:
- Integer(2) -> '2'
- Rational(3,2) -> '3/2'
- float 2.0 -> '2'

Float mode prints decimals:
- Integer(2) -> '2.0'
- Rational(3,2) -> '1.5'
- float 2.0 -> '2.0'

Use set_display_mode('rational'|'float') to change globally.
Optionally use the context manager display_mode('float') for temporary changes.
Environment variable POLYCALC_NUMERIC_OUTPUT can set the default ('float' or 'rational').
"""

from __future__ import annotations

import os
from typing import Any

from polynomials.primitives.polycalc_numbers import Integer, Rational

# Global display mode
DISPLAY_MODE: str = "float"  # default 'float' to match existing outputs


def set_display_mode(mode: str) -> None:
    global DISPLAY_MODE
    if mode not in ("rational", "float"):
        raise ValueError("display mode must be 'rational' or 'float'")
    DISPLAY_MODE = mode


def get_display_mode() -> str:
    return DISPLAY_MODE


def _init_mode_from_env() -> None:
    """Initialize DISPLAY_MODE from environment if provided.
    Respects POLYCALC_NUMERIC_OUTPUT in {'float','rational'} (case-insensitive).
    Invalid values are ignored.
    """
    env = os.environ.get("POLYCALC_NUMERIC_OUTPUT")
    if not env:
        return
    val = env.strip().lower()
    if val in {"float", "rational"}:
        set_display_mode(val)


def format_number(n: Any) -> str:
    """Format numbers consistently based on global DISPLAY_MODE.

    Supports built-in int/float and custom Integer/Rational types.
    Falls back to str(n) for unknown types.
    """
    mode = DISPLAY_MODE

    # Custom exact types first
    if isinstance(n, Integer):
        if mode == "float":
            return f"{float(n)}"
        return str(int(n))

    if isinstance(n, Rational):
        if mode == "float":
            return f"{float(n)}"
        return str(n)

    # Built-in numbers
    if isinstance(n, int):
        return f"{float(n)}" if mode == "float" else str(n)

    if isinstance(n, float):
        if mode == "rational":
            # Show integers without .0
            if n.is_integer():
                return str(int(n))
            return str(n)
        else:
            return str(n)

    # Fallback
    return str(n)


class display_mode:
    """Context manager to temporarily switch display mode.

    Example:
        with display_mode('float'):
            ...
    """

    def __init__(self, mode: str):
        self._prev = get_display_mode()
        set_display_mode(mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        set_display_mode(self._prev)
        return False


# Initialize default from environment, if provided
_init_mode_from_env()
