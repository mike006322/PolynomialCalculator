from polynomial import *
from itertools import combinations
from time import time


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
            if p in res:
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
            if h != 0:
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

    # Solve multivariable polynomials via Groebner basis:
    # 1. Apply up with criteria to tell whether there are finitely many solutions
    #     Criteria: For I in k[x_1, x_2, ..., x_n], V(I) is a finite set if:
    #     - Let G be a Groebner basis for I, then for each i, 1 <= i <= n,
    #       there is some m_i >= 0 such that x_i^(m_i) = LM(g) for some g in G.
    #       For example, Ideal I with groebner basis 3x^2+y+z^2, y^3+z, 4z has finite number of solutions.
    #       To implement this we take the LM of every g in G and check if they are powers of x_i
    #       and check that each x_i is accounted for.
    #       If we use lex order then this guarantees that if there are finite solutions then
    #       we will have an element of the GB that is all of one variable.
    # 2. If so, calculate Groebner basis
    # 3. Evaluate and extend solution

    @staticmethod
    def solvability_criteria(groebner_basis, variables):
        """
        returns boolean whether system has finite number of solutions
        """
        for variable in variables:
            for g in groebner_basis:
                if len(g.LM().variables()) == 1:
                    v = g.LM().variables().pop()
                    if v == variable:
                        break
            else:
                return False
        return True

    @staticmethod
    def find_solutions(groebner_basis, zeroes, solution=None):
        if solution:
            new_groebner_basis = []
            for g in groebner_basis:
                h = g.copy()(**solution)
                if type(h) == Polynomial:
                    if len(h.variables()) != 0:
                        new_groebner_basis.append(h)
            if len(new_groebner_basis) == 0:
                for v in solution:
                    if type(solution[v]) == Integer or type(solution[v]) == Rational:
                        solution[v] = float(solution[v])
                zeroes.add(frozenset(sorted(solution.items())))
            for g in new_groebner_basis:
                if len(g.variables()) == 1:
                    v = g.variables().pop()
                    solutions = solve(g)
                    if type(solutions) == set or type(solutions) == tuple or type(solutions) == list:
                        for s in solutions:
                            new_solution = dict(solution)
                            new_solution[v] = s
                            Ideal.find_solutions(new_groebner_basis, zeroes, new_solution)
                    else:
                        single_solution = solutions
                        new_solution = dict(solution)
                        new_solution[v] = single_solution
                        Ideal.find_solutions(new_groebner_basis, zeroes, new_solution)
                    break
        else:
            for g in groebner_basis:
                if len(g.variables()) == 1:
                    v = g.variables().pop()
                    solutions = solve(g)
                    if type(solutions) == set or type(solutions) == tuple or type(solutions) == list:
                        for s in solutions:
                            solution = {v: s}
                            Ideal.find_solutions(groebner_basis, zeroes, solution)
                    else:
                        solution = {v: solutions}
                        Ideal.find_solutions(groebner_basis, zeroes, solution)
                    break

    def solve_system(self):
        print(self)
        """
        If finite solutions exist, output solutions
        Otherwise output "finite solutions don't exit"
        """
        variables = set()
        for p in self.polynomials:
            variables = variables.union(p.variables())
        variables = sorted(list(variables)) #lex ordering
        groebner_basis = self.groebner_basis()
        print('did GB')
        zeroes = set()
        if not Ideal.solvability_criteria(groebner_basis, variables):
            return "finite solutions don't exit"
        Ideal.find_solutions(groebner_basis, zeroes)
        output_string = str(len(zeroes)) + " solutions: \n"
        for zero in zeroes:
            zero_list = list(zero)
            output_string += '['
            for var in sorted(zero_list):
                output_string += var[0] + ' = ' + str(var[1]) + ', '
            output_string = output_string[:-2]
            output_string += '],\n'
        output_string = output_string[:-2]
        return output_string
