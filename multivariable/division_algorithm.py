import multivariable_polynomial


def divides(a, b):
    """
    returns True if LT(a) has exponents all less than LT(b)
    """
    if a.term_matrix == [[' ']] or b.term_matrix == [[' ']]:
        return False
    a, b = multivariable_polynomial.Polynomial.combine_variables(a, b)
    a = a.term_matrix
    b = b.term_matrix
    res = True
    for i in range(1, len(a[1])):
        if a[1][i] > b[1][i]:
            res = False
    return res


def monomial_divide(a, b):
    a, b = multivariable_polynomial.Polynomial.combine_variables(a, b)
    res = a
    res.term_matrix[1][0] = a.term_matrix[1][0] / b.term_matrix[1][0]
    for i in range(1, len(res.term_matrix[0])):
        for j in range(1, len(res.term_matrix)):
            res.term_matrix[j][i] -= b.term_matrix[j][i]
    return res


def division_algorithm(input_poly, *others):
    """
    input is polynomial/s
    output is first polynomial divided by other polynomial/s and a remainder as Polynomial classes
    """
    # others is an ordered tuple of functions
    a = []
    for i in range(len(others)):
        a.append(multivariable_polynomial.Polynomial(0))
    p = input_poly.copy()
    r = multivariable_polynomial.Polynomial(0)
    while p != multivariable_polynomial.Polynomial(0):
        i = 0
        division_occured = False
        while i < len(others) and division_occured == False:
            if divides(others[i], p):
                a[i] += monomial_divide(p.LT(), others[i].LT())
                p -= monomial_divide(p.LT(), others[i].LT()) * others[i]
                division_occured = True
            else:
                i += 1
        if division_occured == False:
            p_LT = p.LT()
            r += p_LT
            p -= p.LT()
    for poly in a:
        poly.term_matrix = input_poly.mod_poly(poly.term_matrix)
    r.term_matrix = input_poly.mod_poly(r.term_matrix)
    return a, r


def division_string(p, *others):
    """
    input is polynomial/s
    output is string "[p] = ([divisor])*([other polynomial/s]) + ([remainder:]) remainder"
    """
    a, r = division_algorithm(p, *others)
    res = str(p) + ' = '
    for i in range(len(a)):
        res += '(' + str(a[i]) + ')' + '*' + '(' + str(others[i]) + ')' + ' + '
    if res.endswith(" + "):
        res = res[:-3]
    res += ' + (remainder:) ' + str(r)
    return res
