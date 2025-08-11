from typing import List, Sequence, Tuple, Union

Number = Union[int, float, complex]

__all__ = [
    "solve",
    "quadratic_formula",
    "isclose",
    "Durand_Kerner",
]


def solve(polynomial) -> Union[str, Number, Sequence[Number]]:
    """Solve a univariate polynomial using its sparse representation.

    Returns:
        - "too many variables" for multivariate input
        - Numeric root(s) or list of complex approximations for higher degree.
    """
    active_vars = polynomial.variables
    if len(active_vars) > 1:
        return "too many variables"
    # Constant polynomial (no active variable)
    if not active_vars:
        if not polynomial.terms:
            return 0
        if len(polynomial.terms) == 1:
            (m0, c0), = polynomial.terms.items()
            if all(e == 0 for e in m0.exps):
                return c0
        return 0
    var = active_vars[0]
    # Build coefficient list from sparse terms: list of (coeff, exponent)
    coeff_rows: List[Tuple[Number, int]] = []
    for m, c in polynomial.terms.items():
        if var in m.vars:
            idx = m.vars.index(var)
            exp = m.exps[idx]
        else:
            exp = 0
        if c != 0:
            coeff_rows.append((c, exp))
    if not coeff_rows:
        coeff_rows.append((0.0, 0))
    coeff_rows.sort(key=lambda t: t[1], reverse=True)
    degree = coeff_rows[0][1]

    if degree == 0:
        # Constant after all (e.g., all variable terms canceled)
        return coeff_rows[0][0]

    if degree == 1:
        a = None
        b = 0
        for c, e in coeff_rows:
            if e == 1:
                a = c
            elif e == 0:
                b = c
        if a is None or a == 0:
            return 0
        root = -b / a
        try:
            if float(root).is_integer():
                return int(root)
        except Exception:  # pragma: no cover - defensive
            pass
        return root

    if degree == 2:
        # Reconstruct minimal pseudo term_matrix for quadratic_formula compatibility
        a = b = c0 = 0
        for coeff, exp in coeff_rows:
            if exp == 2:
                a = coeff
            elif exp == 1:
                b = coeff
            elif exp == 0:
                c0 = coeff
        class _Wrapper:  # pragma: no cover - simple container
            term_matrix = [["constant", var]] + [[a, 2], [b, 1], [c0, 0]]
        return quadratic_formula(_Wrapper)  # type: ignore[arg-type]

    if degree > 2:
        # Wrapper for Durand-Kerner expecting degree() and __call__
        class _Wrapper2:  # pragma: no cover - iterative numeric method
            def degree(self):
                return degree
            def __call__(self, x):
                res: Number = 0
                for coeff, exp in coeff_rows:
                    res += coeff * (x ** exp)  # type: ignore[operator]
                return res
        return Durand_Kerner(_Wrapper2())

    # Fallback (shouldn't reach here)
    return 0


def quadratic_formula(polynomial) -> Union[Number, Tuple[Number, Number]]:
    """
    input is single-variable polynomial of degree 2
    returns zeros
    """
    if len(polynomial.term_matrix) == 3:
        if polynomial.term_matrix[2][1] == 1:
            a, b = polynomial.term_matrix[1][0], polynomial.term_matrix[2][0]
            return 0, -b / a
        a, c = polynomial.term_matrix[1][0], polynomial.term_matrix[2][0]
        return (-c / a) ** 0.5, -((-c / a) ** 0.5)
    if len(polynomial.term_matrix) == 2:
        (
            a,
            b,
            c,
        ) = (
            polynomial.term_matrix[1][0],
            0,
            0,
        )
    elif len(polynomial.term_matrix) == 3:
        a, b, c = polynomial.term_matrix[1][0], polynomial.term_matrix[2][0], 0
    else:
        a, b, c = (
            polynomial.term_matrix[1][0],
            polynomial.term_matrix[2][0],
            polynomial.term_matrix[3][0],
        )
    denom = 2 * a
    ans1 = (-b + (b**2 - 4 * a * c) ** 0.5) / denom
    ans2 = (-b - (b**2 - 4 * a * c) ** 0.5) / denom
    if ans1 == ans2:
        return ans1
    return ans1, ans2


def isclose(a: Number, b: Number, rel_tol: float = 1e-09, abs_tol: float = 0.0001) -> bool:
    """
    returns boolean whether abs(a-b) is less than abs_total or rel_total*max(a, b)
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def Durand_Kerner(f) -> List[complex]:
    """
    input polynomial
    returns numerical approximation of all complex roots
    """
    roots: List[complex] = []
    for i in range(f.degree()):
        roots.append((0.4 + 0.9j) ** i)
    diff: float = 1
    diff_temp: float = 0

    def iterate() -> None:
        nonlocal roots
        new_roots = roots[:]
        for i in range(len(roots)):
            q: complex = 1
            for j, root in enumerate(roots):
                if j != i:
                    q *= roots[i] - root
            new_roots[i] = roots[i] - f(roots[i]) / q
        nonlocal diff
        nonlocal diff_temp
        diff_temp = diff
        diff = 0
        for i in range(len(roots)):
            diff += abs(roots[i] - new_roots[i])
        roots = new_roots

    while diff > 0.00000001 and not isclose(diff_temp, diff):
        iterate()
    for i in range(len(roots)):
        if isclose(roots[i].real, round(roots[i].real)):
            temp = round(roots[i].real)
            roots[i] -= roots[i].real
            roots[i] += temp
        if isclose(roots[i].imag, round(roots[i].imag)):
            temp = round(roots[i].imag)
            roots[i] -= roots[i].imag * 1j
            roots[i] += temp * 1j
    return roots


if __name__ == "__main__":
    pass
