from core.polynomial import *


class Ideal:

    def __init__(self, *polynomials):
        self.polynomials = polynomials

    def groebner_basis(self):
        pass

    @staticmethod
    def s_polynomial(f, g):
        """
        S(f, g) = (x^gamma / LT(f)) * f - (x^gamma / LT(g)) * g
        x^gamma = least_common_multiple(leading_monomial(f), leading_monomial(g))
        """
        return (lcm(f.LT(), g.LT())/f.LT())*f - (lcm(f.LT(), g.LT())/g.LT())*g
