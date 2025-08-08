#!/usr/bin/env python3
"""
PolynomialCalculator Command Line Interface.

Provides command-line access to polynomial operations, finite field computations,
and algebraic operations.
"""

import argparse
import json
import logging
import sys
from typing import List, Optional

from polynomials.display import format_number, set_display_mode

# Lazily resolve package version without importing the top-level package
# Prefer importlib.metadata when installed; fallback to local version module.


def _get_version() -> str:
    try:
        try:
            from importlib import metadata as importlib_metadata  # Py>=3.8
        except Exception:
            import importlib_metadata  # type: ignore
        try:
            return importlib_metadata.version("PolynomialCalculator")
        except Exception:
            pass
    except Exception:
        pass
    # Fallbacks for source checkouts / editable installs
    # 1) Try plain import from project root if on sys.path
    try:
        from version import __version__  # type: ignore

        return __version__
    except Exception:
        # 2) Load version.py by absolute path relative to this file
        try:
            import importlib.util
            from pathlib import Path

            root = Path(__file__).resolve().parents[2]
            vp = root / "version.py"
            if vp.exists():
                spec = importlib.util.spec_from_file_location("_pc_version", str(vp))
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    v = getattr(mod, "__version__", None)  # type: ignore[attr-defined]
                    if isinstance(v, str):
                        return v
        except Exception:
            pass
    return "unknown"


# Early parse of version and display flags


def _early_handle_global_flags(argv: List[str]) -> Optional[int]:
    # --version fast-path
    if "--version" in argv or "-V" in argv:
        print(f"polycalc {_get_version()}")
        return 0
    # Numeric output mode flags
    if "--float" in argv and "--rational" in argv:
        print("Error: --float and --rational are mutually exclusive", file=sys.stderr)
        return 2
    if "--numeric-output" in argv:
        try:
            idx = argv.index("--numeric-output")
            mode = argv[idx + 1]
            set_display_mode(mode)
            # Strip the pair so argparse doesn't see it twice
            del argv[idx : idx + 2]
        except Exception:
            print("Error: --numeric-output requires an argument: rational|float", file=sys.stderr)
            return 2
    # Convenience flags
    if "--float" in argv:
        set_display_mode("float")
        argv.remove("--float")
    if "--rational" in argv:
        set_display_mode("rational")
        argv.remove("--rational")
    return None


def main() -> int:
    """Main entry point for the polycalc command-line tool."""
    argv: List[str] = sys.argv[1:]
    early = _early_handle_global_flags(argv)
    if isinstance(early, int):
        return early

    parser = argparse.ArgumentParser(
        description="PolynomialCalculator CLI: Finite field and polynomial operations",
        prog="polycalc",
    )
    # Global flags (help only; already handled early)
    parser.add_argument("--version", action="version", version=f"%(prog)s {_get_version()}")
    parser.add_argument(
        "--numeric-output", choices=["rational", "float"], help="Numeric display mode"
    )
    parser.add_argument("--float", action="store_true", help="Shortcut for --numeric-output float")
    parser.add_argument(
        "--rational", action="store_true", help="Shortcut for --numeric-output rational"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose debug logging")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-error output")
    parser.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON (solve, solve-system)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: create finite field
    ff_parser = subparsers.add_parser(
        "finite_field", help="Create a finite field and show Zech logarithm table info"
    )
    ff_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")
    ff_parser.add_argument("i", type=int, help="Field degree i (GF(p^i))")

    # Subcommand: random monic polynomial
    monic_parser = subparsers.add_parser(
        "random_monic", help="Generate a random monic polynomial of degree n over F_p"
    )
    monic_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")
    monic_parser.add_argument("n", type=int, help="Degree n")

    # Subcommand: find irreducible polynomial
    irr_parser = subparsers.add_parser(
        "find_irreducible", help="Find an irreducible polynomial of degree n over F_p"
    )
    irr_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")
    irr_parser.add_argument("n", type=int, help="Degree n")

    # Subcommand: gcd of two polynomials
    gcd_parser = subparsers.add_parser("gcd", help="Compute GCD of two polynomials over F_p")
    gcd_parser.add_argument("poly1", type=str, help="First polynomial (as string, e.g. 'x^2+1')")
    gcd_parser.add_argument("poly2", type=str, help="Second polynomial (as string)")
    gcd_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")

    # Subcommand: solve polynomial equation
    solve_parser = subparsers.add_parser(
        "solve", help="Solve a univariate polynomial equation over the rationals"
    )
    solve_parser.add_argument("poly", type=str, help="Polynomial equation as string, e.g. 'x^2-2'")
    solve_parser.add_argument(
        "var", type=str, default="x", nargs="?", help="Variable to solve for (default: x)"
    )

    # Subcommand: Groebner basis
    groebner_parser = subparsers.add_parser(
        "groebner", help="Compute Groebner basis for a list of polynomials"
    )
    groebner_parser.add_argument(
        "polys", nargs="+", type=str, help="List of polynomials as strings, e.g. 'x^2+y^2-1' 'x-y'"
    )
    groebner_parser.add_argument(
        "--vars", nargs="+", type=str, default=["x", "y"], help="Variables (default: x y)"
    )
    groebner_parser.add_argument(
        "--order",
        choices=["lex", "grlex", "grevlex"],
        default="lex",
        help="Monomial order to use (default: lex)",
    )

    # Subcommand: solve-system (structured)
    solve_sys_parser = subparsers.add_parser(
        "solve-system",
        help="Solve a multivariate system using Groebner basis; returns structured solutions",
    )
    solve_sys_parser.add_argument(
        "polys", nargs="+", type=str, help="List of polynomials as strings"
    )

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # Propagate argparse's intended exit code (e.g., --help errors => 2)
        return e.code if isinstance(e.code, int) else 1

    try:
        # Configure logging based on flags
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
        elif args.quiet:
            logging.basicConfig(level=logging.ERROR, format="%(levelname)s:%(name)s:%(message)s")
        else:
            logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")

        def _to_json_value(val):
            try:
                import numbers

                if isinstance(val, numbers.Integral):
                    return int(val)
                if isinstance(val, numbers.Real) and not isinstance(val, bool):
                    # Keep as float (covers float and Decimal-real-ish)
                    return float(val)
            except Exception:
                pass
            # Fallback to string formatting used by display module
            try:
                return format_number(val)
            except Exception:
                return str(val)

        if args.command == "finite_field":
            # Lazy import to avoid optional heavy deps at module import time
            try:
                from algebra.construct_finite_field import ZechLogarithmTable
            except ImportError:
                print(
                    "Error: Finite field features require optional dependencies. "
                    "Install extras: pip install 'PolynomialCalculator[algebra]'",
                    file=sys.stderr,
                )
                return 1
            table = ZechLogarithmTable(args.p, args.i)
            print(f"Created GF({args.p}^{args.i}) with irreducible polynomial: {table.h}")
            print(f"Primitive element table size: {len(table.poly_to_power)} elements")

        elif args.command == "random_monic":
            try:
                from algebra.construct_finite_field import random_monic
            except ImportError:
                print(
                    "Error: Random monic requires optional dependencies. "
                    "Install extras: pip install 'PolynomialCalculator[algebra]'",
                    file=sys.stderr,
                )
                return 1
            poly = random_monic(args.p, args.n)
            print(f"Random monic polynomial over F_{args.p} of degree {args.n}: {poly}")

        elif args.command == "find_irreducible":
            try:
                from algebra.construct_finite_field import find_irreducible
            except ImportError:
                print(
                    "Error: Finding irreducibles requires optional dependencies. "
                    "Install extras: pip install 'PolynomialCalculator[algebra]'",
                    file=sys.stderr,
                )
                return 1
            poly = find_irreducible(args.p, args.n)
            print(f"Irreducible polynomial over F_{args.p} of degree {args.n}: {poly}")

        elif args.command == "gcd":
            # Lazy import core polynomial machinery
            from polynomials.polynomial import Polynomial, gcd

            poly1 = Polynomial(args.poly1, args.p)
            poly2 = Polynomial(args.poly2, args.p)
            result = gcd(poly1, poly2)
            print(f"gcd({poly1}, {poly2}) = {result}")

        elif args.command == "solve":
            # Lazy import core polynomial machinery
            from polynomials.polynomial import Polynomial

            poly = Polynomial(args.poly)
            sol = poly.solve()
            if args.json:
                if isinstance(sol, (list, tuple)):
                    solutions_payload = [_to_json_value(s) for s in sol]
                else:
                    solutions_payload = [_to_json_value(sol)]
                payload = {
                    "command": "solve",
                    "poly": args.poly,
                    "var": args.var,
                    "solutions": solutions_payload,
                    "count": len(solutions_payload),
                    "status": "ok",
                }
                print(json.dumps(payload))
            else:
                print(f"Solutions to {args.poly} = 0:")
                if isinstance(sol, (list, tuple)):
                    for s in sol:
                        try:
                            from polynomials.polynomial import Polynomial as _Poly

                            is_poly = isinstance(s, _Poly)
                        except Exception:
                            is_poly = False
                        print(f"  {s if is_poly else format_number(s)}")
                else:
                    try:
                        from polynomials.polynomial import Polynomial as _Poly

                        is_poly = isinstance(sol, _Poly)
                    except Exception:
                        is_poly = False
                    print(f"  {sol if is_poly else format_number(sol)}")

        elif args.command == "groebner":
            # Apply selected monomial order globally for Polynomial operations
            import polynomials.orderings as ord
            import polynomials.polynomial as poly_mod

            if args.order == "lex":
                poly_mod.order = ord.order_lex
            elif args.order == "grlex":
                poly_mod.order = ord.graded_lex
            else:  # grevlex
                # grevlex function name is grev_lex
                poly_mod.order = ord.grev_lex
            # Now construct polynomials and compute Groebner basis
            from polynomials.ideal import Ideal
            from polynomials.polynomial import Polynomial

            polys = [Polynomial(p) for p in args.polys]
            ideal = Ideal(*polys)
            G = ideal.groebner_basis()
            if args.json:
                payload = {
                    "command": "groebner",
                    "polys": args.polys,
                    "order": args.order,
                    "status": "ok",
                    "basis": [str(g) for g in G],
                    "count": len(G),
                }
                print(json.dumps(payload))
            else:
                print("Groebner basis:")
                for g in G:
                    print(f"  {g}")

        elif args.command == "solve-system":
            from polynomials.ideal import Ideal
            from polynomials.polynomial import Polynomial

            polys = [Polynomial(p) for p in args.polys]
            ideal = Ideal(*polys)
            solutions = ideal.solve_system_structured()
            if args.json:
                if solutions is None:
                    payload = {
                        "command": "solve-system",
                        "polys": args.polys,
                        "status": "undetermined",
                        "solutions": None,
                        "count": None,
                    }
                elif not solutions:
                    payload = {
                        "command": "solve-system",
                        "polys": args.polys,
                        "status": "no_solutions",
                        "solutions": [],
                        "count": 0,
                    }
                else:
                    norm_solutions = []
                    for sol in solutions:
                        norm_solutions.append({k: _to_json_value(v) for k, v in sol.items()})
                    payload = {
                        "command": "solve-system",
                        "polys": args.polys,
                        "status": "ok",
                        "solutions": norm_solutions,
                        "count": len(norm_solutions),
                    }
                print(json.dumps(payload))
            else:
                if solutions is None:
                    print("No finite number of solutions (undetermined/infinite)")
                elif not solutions:
                    print("0 solutions")
                else:
                    print(f"{len(solutions)} solutions:")
                    for sol in solutions:
                        ordered = ", ".join(
                            f"{k} = {format_number(sol[k])}" for k in sorted(sol.keys())
                        )
                        print(f"  [ {ordered} ]")

        else:
            parser.print_help()
            return 1

        return 0

    except Exception as e:
        if "args" in locals() and getattr(args, "json", False):
            err_payload = {
                "status": "error",
                "error": str(e),
            }
            print(json.dumps(err_payload))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
