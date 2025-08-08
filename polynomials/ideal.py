from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union
from polynomials.polynomial import Polynomial, lcm, division_algorithm
from polynomials.primitives.polycalc_numbers import Integer, Rational
from itertools import combinations

# Numeric types used in solutions/coefficients
NumberLike = Union[Integer, Rational, int, float]


class Ideal:

    def __init__(self, *polynomials: Polynomial) -> None:
        self.polynomials: Tuple[Polynomial, ...] = polynomials

    def __eq__(self, other: Any) -> bool:
        """
        Two ideals are equal if they have the same Groebner basis up to constant multiple
        """
        g = self.groebner_basis()
        for poly in other.groebner_basis():
            if poly not in g and (-1) * poly not in g:
                return False
        return True

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        res = '<'
        for p in self.polynomials:
            res += str(p) + ', '
        return res[:-2] + '>'

    @staticmethod
    def s_polynomial(f: Polynomial, g: Polynomial) -> Polynomial:
        """
        S(f, g) = (x^gamma / LT(f)) * f - (x^gamma / LT(g)) * g
        x^gamma = least_common_multiple(leading_monomial(f), leading_monomial(g))
        """
        return (lcm(f.LT(), g.LT()) / f.LT()) * f - (lcm(f.LT(), g.LT()) / g.LT()) * g

    @staticmethod
    def minimize(G: Iterable[Polynomial]) -> List[Polynomial]:
        """
        LC(p) = 1 for all p ∈ G
        For all p ∈ G, no monomial of p lies in <LT(G −{p})>
        """
        res = list(G)
        extra: List[Polynomial] = list()
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
    def reduce(G: Iterable[Polynomial]) -> List[Polynomial]:
        """
        input minimum basis for G
        output reduced basis
        http://pi.math.cornell.edu/~dmehrle/notes/old/alggeo/15BuchbergersAlgorithm.pdf
        """
        res = list(G)
        for i in range(len(G)):
            res.remove(G[i])
            # Apply division algorithm against each polynomial in res
            h = G[i]
            if res:  # Only if there are polynomials to divide by
                _, h = division_algorithm(h, *res)
            if h != 0:
                res = [h] + res
        return res

    def groebner_basis(self) -> List[Polynomial]:
        """
        returns reduced groebner basis
        """
        B: Set[Tuple[int, int]] = set(combinations(range(len(self.polynomials)), 2))
        G = Ideal.reduce(list(self.polynomials))
        F: List[Optional[Polynomial]] = list(self.polynomials)
        # test if this modifies self.polynomials
        # polynomials are indexed 0 to s
        s = len(self.polynomials) - 1
        t = 0
        while B:
            (i, j) = B.pop()
            if lcm(F[i].LT(), F[j].LT()) != F[i].LT() * F[j].LT() and not self.criterion(i, j, B):
                S_poly = Ideal.s_polynomial(F[i], F[j])
                # Reduce S_poly by the polynomials in G using division algorithm
                if G:  # Only if there are polynomials to divide by
                    _, S = division_algorithm(S_poly, *G)
                else:
                    S = S_poly
                if S != 0:
                    t += 1
                    # Extend F if necessary
                    while len(F) <= t:
                        F.append(None)
                    F[t] = S
                    G.append(F[t])
                    # reduce G as we are adding to it
                    G = Ideal.reduce(G)
                    G = Ideal.minimize(G)
                    B = B.union(set(combinations(range(t - 1), 2)))
        return G

    def criterion(self, i: int, j: int, B: Set[Tuple[int, int]]) -> bool:
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
    def solvability_criteria(groebner_basis: Iterable[Polynomial], variables: Iterable[str]) -> bool:
        """
        returns boolean whether system has finite number of solutions
        """
        for variable in variables:
            for g in groebner_basis:
                if len(g.LM().variables) == 1:
                    v = g.LM().variables.pop()
                    if v == variable:
                        break
            else:
                return False
        return True

    @staticmethod
    def find_solutions(
        groebner_basis: Iterable[Polynomial],
        zeroes: Set[frozenset],
        solution: Optional[Dict[str, NumberLike]] = None,
    ) -> None:
        if solution:
            # key could be Variable type, so convert to string which is necessary for **
            solution = {str(key): value for key, value in solution.items()}
            new_groebner_basis: List[Polynomial] = []
            for g in groebner_basis:
                h = g.copy()(**solution)
                if type(h) == Polynomial:
                    if len(h.variables) != 0:
                        new_groebner_basis.append(h)
            if len(new_groebner_basis) == 0:
                for v in solution:
                    if type(solution[v]) == Integer or type(solution[v]) == Rational:
                        solution[v] = float(solution[v])
                zeroes.add(frozenset(sorted(solution.items())))
            for g in new_groebner_basis:
                if len(g.variables) == 1:
                    v = g.variables.pop()
                    solutions = g.solve()
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
                if len(g.variables) == 1:
                    v = g.variables.pop()
                    solutions = g.solve()
                    if type(solutions) == set or type(solutions) == tuple or type(solutions) == list:
                        for s in solutions:
                            solution = {v: s}
                            Ideal.find_solutions(groebner_basis, zeroes, solution)
                    else:
                        solution = {v: solutions}
                        Ideal.find_solutions(groebner_basis, zeroes, solution)
                    break

    def solve_system(self) -> str:
        """
        If finite solutions exist, output solutions
        Otherwise output "finite solutions don't exit"
        """
        variables: Set[str] = set()
        for p in self.polynomials:
            variables = variables.union(p.variables)
        variables_list = sorted(list(variables))  # lex ordering
        groebner_basis = self.groebner_basis()
        zeroes: Set[frozenset] = set()
        if not Ideal.solvability_criteria(groebner_basis, variables_list):
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

    def solve_system_structured(self) -> Optional[List[Dict[str, NumberLike]]]:
        """Return solutions as a structured list of dictionaries.
        Each dict maps variable name (str) to a numeric value (Integer/Rational/int/float).
        If the system does not have finitely many solutions, return None.
        """
        variables: Set[str] = set()
        for p in self.polynomials:
            variables = variables.union(p.variables)
        variables_list = sorted(list(variables))  # lex ordering
        groebner_basis = self.groebner_basis()
        zeroes: Set[frozenset] = set()
        if not Ideal.solvability_criteria(groebner_basis, variables_list):
            return None
        Ideal.find_solutions(groebner_basis, zeroes)
        solutions: List[Dict[str, NumberLike]] = []
        for zero in zeroes:
            as_dict = dict(zero)
            # Ensure stable key order; keep exact types
            clean: Dict[str, NumberLike] = {}
            for k in sorted(as_dict.keys()):
                v = as_dict[k]
                clean[str(k)] = v  # type: ignore[assignment]
            solutions.append(clean)
        # Sort list of solutions deterministically using float as key only
        def key_fn(d: Dict[str, NumberLike]):
            def to_float(x: NumberLike) -> float:
                if isinstance(x, (Integer, Rational)):
                    return float(x)
                return float(x)
            return tuple(to_float(d.get(k)) for k in variables_list)
        solutions.sort(key=key_fn)  # type: ignore[arg-type]
        return solutions
