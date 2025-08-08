from typing import List, Sequence, Tuple, Union

Number = Union[int, float, complex]


def solve(polynomial) -> Union[str, Number, Sequence[Number]]:
    """
    input is polynomial
    if more than one variable, returns 'too many variables'
    looks for formula to apply to coefficients
    returns solution or 'I cannot solve yet...'
    """
    if len(polynomial.term_matrix[0]) > 2:
        return "too many variables"
    elif len(polynomial.term_matrix[0]) == 1:
        return polynomial.term_matrix[1][0]
    elif len(polynomial.term_matrix[0]) == 2:
        degree = polynomial.term_matrix[1][1]
        if degree == 1:
            if len(polynomial.term_matrix) == 2:
                return 0
            else:
                return -polynomial.term_matrix[2][0] / polynomial.term_matrix[1][0]
        if degree == 2:
            ans = quadratic_formula(polynomial)
            return ans
        if degree > 2:
            return Durand_Kerner(polynomial)


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
    ans1 = (-b + (b**2 - 4 * a * c) ** 0.5) / 2 * a
    ans2 = (-b - (b**2 - 4 * a * c) ** 0.5) / 2 * a
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
