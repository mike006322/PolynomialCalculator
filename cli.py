import argparse
from core.number_objects.polynomial import Polynomial, gcd
from construct_finite_field import ZechLogarithmTable, random_monic, find_irreducible, find_primitive_element


def main():
    parser = argparse.ArgumentParser(
        description="Polynomial Calculator CLI: Finite field and polynomial operations"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: create finite field
    ff_parser = subparsers.add_parser("finite_field", help="Create a finite field and show Zech logarithm table info")
    ff_parser.add_argument("p", type=int, help="Prime characteristic p")
    ff_parser.add_argument("i", type=int, help="Field degree i (GF(p^i))")

    # Subcommand: random monic polynomial
    monic_parser = subparsers.add_parser("random_monic", help="Generate a random monic polynomial of degree n over F_p")
    monic_parser.add_argument("p", type=int, help="Prime characteristic p")
    monic_parser.add_argument("n", type=int, help="Degree n")

    # Subcommand: find irreducible polynomial
    irr_parser = subparsers.add_parser("find_irreducible", help="Find an irreducible polynomial of degree n over F_p")
    irr_parser.add_argument("p", type=int, help="Prime characteristic p")
    irr_parser.add_argument("n", type=int, help="Degree n")

    # Subcommand: gcd of two polynomials
    gcd_parser = subparsers.add_parser("gcd", help="Compute GCD of two polynomials over F_p")
    gcd_parser.add_argument("poly1", type=str, help="First polynomial (as string, e.g. 'x^2+1')")
    gcd_parser.add_argument("poly2", type=str, help="Second polynomial (as string)")
    gcd_parser.add_argument("p", type=int, help="Prime characteristic p")
