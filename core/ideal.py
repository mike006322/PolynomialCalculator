from core.polynomial import *
from itertools import combinations


class Ideal:

    def __init__(self, *polynomials):
        self.polynomials = polynomials

    def __eq__(self, other):
        """
        Two ideals are equal if they have the same Groebner basis up to constant multiple
        """
        g = self.groebner_basis()
        for poly in other.groebner_basis():
            if poly not in g and (-1)*poly not in g:
                return False
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        res = '<'
        for p in self.polynomials:
            res += str(p) + ', '
        return res[:-2] + '>'

    @staticmethod
    def s_polynomial(f, g):
        """
        S(f, g) = (x^gamma / LT(f)) * f - (x^gamma / LT(g)) * g
        x^gamma = least_common_multiple(leading_monomial(f), leading_monomial(g))
        """
        return (lcm(f.LT(), g.LT())/f.LT())*f - (lcm(f.LT(), g.LT())/g.LT())*g

    @staticmethod
    def minimize(G):
        """
        LC(p) = 1 for all p ∈ G
        For all p ∈ G, no monomial of p lies in <LT(G −{p})>
        """
        res = list(G)
        extra = list()
        for p in res:
            for term in p.terms():
                for q in res:
                    if p != q:
                        if term % q.LT() == 0:
                            extra.append(p)
        for p in extra:
            res.remove(p)
        return res

    @staticmethod
    def reduce(G):
        """
        input minimum basis for G
        output reduced basis
        http://pi.math.cornell.edu/~dmehrle/notes/old/alggeo/15BuchbergersAlgorithm.pdf
        """
        res = list(G)
        for i in range(len(G)):
            res.remove(G[i])
            h = G[i] % res
            res = [h] + res
        return res

    def groebner_basis(self):
        """
        returns reduced groebner basis
        """
        B = set(combinations(range(len(self.polynomials)), 2))
        G = Ideal.reduce(list(self.polynomials))
        F = list(self.polynomials)
        # test if this modifies self.polynomials
        # polynomials are indexed 0 to s
        s = len(self.polynomials) - 1
        t = 0
        while B:
            (i, j) = B.pop()
            if lcm(F[i].LT(), F[j].LT()) != F[i].LT()*F[j].LT() and not self.criterion(i, j, B):
                S = Ideal.s_polynomial(F[i], F[j]) % G
                if S != 0:
                    t += 1
                    F[t] = S
                    G.append(F[t])
                    # reduce G as we are adding to it
                    G = Ideal.reduce(G)
                    G = Ideal.minimize(G)
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

