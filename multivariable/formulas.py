def solve(polynomial):
    if len(polynomial.termMatrix[0]) > 2:
        return 'too many variables'
    elif len(polynomial.termMatrix[0]) == 1:
        return polynomial.termMatrix[1][0]
    elif len(polynomial.termMatrix[0]) == 2:
        degree = polynomial.termMatrix[1][1]
        if degree == 1:
            if len(polynomial.termMatrix) == 2:
                return 0
            else:
                return -polynomial.termMatrix[2][0]/polynomial.termMatrix[1][0]
        if degree == 2:
            ans = quadratic_formula(polynomial)
            return ans
        if degree > 2:
            return 'I cannot solve yet...'

def quadratic_formula(polynomial):
    if len(polynomial.termMatrix) == 3:
        a, c = polynomial.termMatrix[1][0], polynomial.termMatrix[2][0]
        return (-c/a)**.5
    a, b, c = polynomial.termMatrix[1][0], polynomial.termMatrix[2][0], polynomial.termMatrix[3][0]
    ans1 = (-b + (b**2 - 4*a*c)**.5)/2*a
    ans2 = (-b - (b**2 - 4*a*c)**.5)/2*a
    if ans1 == ans2:
        return ans1
    return ans1, ans2

if __name__ == '__main__':
    pass
