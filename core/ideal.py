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
        # one can modify this algorithm so that it will automatically produce a reduced Groebner basis.
        # i.e. unique up to constant factors
        # The basic idea is to systematically reduce G each time it is enlarged
        """
        B = set(combinations(range(len(self.polynomials)), 2))
        G = list(self.polynomials)
        F = list(self.polynomials)
        # test if this modifies self.polynomials
        # polynomials are indexed 0 to s
        s = len(self.polynomials) - 1
        t = 0
        while B:
            (i, j) = B.pop()
            if lcm(F[i].LT(), F[j].LT()) != F[i].LT()*F[j].LT() and not self.criterion(i, j, B):
                S = Ideal.s_polynomial(F[i], F[j]) % G
                if s != 0:
                    t += 1
                    F[t] = S
                    # reduce G as we are adding to it
                    G.append(F[t])
                    B = B.union(set(combinations(range(t - 1), 2)))
        return G

    def criterion(self, i, j, B):
        """
        # Criterion( fi, f j, B) is true provided that there is some k not in {i, j}
        # for which the pairs (i,k) and (j,k) are not in B and LT(fk) divides LCM(LT(fi), LT(fj)).
        """
        F = self.polynomials
        for k in range(len(F)):
            if k == i or k == j:
                continue
            elif (i, k) in B or (j, k) in B or (k, i) in B or (k, j) in B:
                continue
            elif F[k].LT() % lcm(F[i].LT(), F[j].LT()) == 0:
                return True
        return False

