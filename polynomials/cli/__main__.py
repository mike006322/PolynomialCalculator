#!/usr/bin/env python3
"""
Main entry point for running polynomials.cli as a module.

This allows the CLI to be executed with `python -m polynomials.cli`.
"""

from polynomials.cli.cli import main

if __name__ == "__main__":
    exit(main())
