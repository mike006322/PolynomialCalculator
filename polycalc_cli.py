#!/usr/bin/env python3
import argparse
from core.number_objects.polynomial import Polynomial, gcd
from core.number_objects.ideal import Ideal
from construct_finite_field import ZechLogarithmTable, random_monic, find_irreducible, find_primitive_element

# Entry point for PolyCalc CLI (renamed from cli.py)

def main():
    parser = argparse.ArgumentParser(
        description="PolyCalc CLI: Finite field and polynomial operations"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: create finite field
    ff_parser = subparsers.add_parser("finite_field", help="Create a finite field and show Zech logarithm table info")
    ff_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")
    ff_parser.add_argument("i", type=int, help="Field degree i (GF(p^i))")

    # Subcommand: random monic polynomial
    monic_parser = subparsers.add_parser("random_monic", help="Generate a random monic polynomial of degree n over F_p")
    monic_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")
    monic_parser.add_argument("n", type=int, help="Degree n")

    # Subcommand: find irreducible polynomial
    irr_parser = subparsers.add_parser("find_irreducible", help="Find an irreducible polynomial of degree n over F_p")
    irr_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")
    irr_parser.add_argument("n", type=int, help="Degree n")

    # Subcommand: gcd of two polynomials
    gcd_parser = subparsers.add_parser("gcd", help="Compute GCD of two polynomials over F_p")
    gcd_parser.add_argument("poly1", type=str, help="First polynomial (as string, e.g. 'x^2+1')")
    gcd_parser.add_argument("poly2", type=str, help="Second polynomial (as string)")
    gcd_parser.add_argument("-p", type=int, default=0, help="Prime characteristic p (default: 0)")


    # Subcommand: solve polynomial equation
    solve_parser = subparsers.add_parser("solve", help="Solve a univariate polynomial equation over the rationals")
    solve_parser.add_argument("poly", type=str, help="Polynomial equation as string, e.g. 'x^2-2'")
    solve_parser.add_argument("var", type=str, default="x", help="Variable to solve for (default: x)")

    # Subcommand: Groebner basis
    groebner_parser = subparsers.add_parser("groebner", help="Compute Groebner basis for a list of polynomials")
    groebner_parser.add_argument("polys", nargs='+', type=str, help="List of polynomials as strings, e.g. 'x^2+y^2-1 x-y' ")
    groebner_parser.add_argument("vars", nargs='+', type=str, default=["x", "y"], help="Variables (default: x y)")

    args = parser.parse_args()

    if args.command == "finite_field":
        table = ZechLogarithmTable(args.p, args.i)
        print(f"Created GF({args.p}^{args.i}) with irreducible polynomial: {table.h}")
        print(f"Primitive element table size: {len(table.poly_to_power)} elements")
    elif args.command == "random_monic":
        poly = random_monic(args.p, args.n)
        print(f"Random monic polynomial over F_{args.p} of degree {args.n}: {poly}")
    elif args.command == "find_irreducible":
        poly = find_irreducible(args.p, args.n)
        print(f"Irreducible polynomial over F_{args.p} of degree {args.n}: {poly}")
    elif args.command == "gcd":
        poly1 = Polynomial(args.poly1, args.p)
        poly2 = Polynomial(args.poly2, args.p)
        result = gcd(poly1, poly2)
        print(f"gcd({poly1}, {poly2}) = {result}")
    elif args.command == "solve":
        # Use the project's Polynomial class to solve
        poly = Polynomial(args.poly)
        sol = poly.solve()
        print(f"Solutions to {args.poly} = 0:")
        if isinstance(sol, (list, tuple)):
            for s in sol:
                print(s)
        else:
            print(sol)
    elif args.command == "groebner":
        # Use the project's Ideal.groebner_basis()
        polys = [Polynomial(p) for p in args.polys]
        I = Ideal(*polys)
        G = I.groebner_basis()
        print("Groebner basis:")
        for g in G:
            print(g)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
