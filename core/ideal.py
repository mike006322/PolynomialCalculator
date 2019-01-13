from core.polynomial import *
from itertools import combinations


class Ideal:

    def __init__(self, *polynomials):
        self.polynomials = polynomials

    @staticmethod
    def s_polynomial(f, g):
        """
        S(f, g) = (x^gamma / LT(f)) * f - (x^gamma / LT(g)) * g
        x^gamma = least_common_multiple(leading_monomial(f), leading_monomial(g))
        """
        return (lcm(f.LT(), g.LT())/f.LT())*f - (lcm(f.LT(), g.LT())/g.LT())*g

    def groebner_basis(self):
        """
        returns groebner basis for self.polynomials
        # need to implement reduced groebner basis
        """
        G = list(self.polynomials)
        G_prime = [0]
        while G_prime != G:
            G_prime = G
            # FOR each pair{p,q}, p != q in G_prime DO
            for p, q in combinations(G_prime, 2):
                S = Ideal.s_polynomial(p, q) % G_prime
                if S != 0:
                    G.append(S)
        return G
