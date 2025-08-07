#!/usr/bin/env python3
"""
Polycalc command-line tool entry point.

This script simulates the installed 'polycalc' command and can be used
until the package is properly installed.
"""

import sys
import os

# Add the current directory to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from polynomials.cli import main

if __name__ == "__main__":
    sys.exit(main())
