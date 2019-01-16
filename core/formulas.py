def solve(polynomial):
    """
    input is polynomial
    if more than one variable, returns 'too many variables'
    looks for formula to apply to coefficients
    returns solution or 'I cannot solve yet...'
    """
    if len(polynomial.term_matrix[0]) > 2:
        return 'too many variables'
    elif len(polynomial.term_matrix[0]) == 1:
        return polynomial.term_matrix[1][0]
    elif len(polynomial.term_matrix[0]) == 2:
        degree = polynomial.term_matrix[1][1]
        if degree == 1:
            if len(polynomial.term_matrix) == 2:
                return 0
            else:
                return -polynomial.term_matrix[2][0]/polynomial.term_matrix[1][0]
        if degree == 2:
            ans = quadratic_formula(polynomial)
            return ans
        if degree > 2:
            return 'I cannot solve yet...'


def quadratic_formula(polynomial):
    """
    input is single-variable polynomial of degree 2
    returns zeros
    """
    if len(polynomial.term_matrix) == 3:
        a, c = polynomial.term_matrix[1][0], polynomial.term_matrix[2][0]
        return (-c/a)**.5, -(-c/a)**.5
    a, b, c = polynomial.term_matrix[1][0], polynomial.term_matrix[2][0], polynomial.term_matrix[3][0]
    ans1 = (-b + (b**2 - 4*a*c)**.5)/2*a
    ans2 = (-b - (b**2 - 4*a*c)**.5)/2*a
    if ans1 == ans2:
        return ans1
    return ans1, ans2


if __name__ == '__main__':
    pass
