import multivariable_polynomial

def divides(A, B):
    """
    returns True if LT(a) has exponents all less than LT(b)
    """
    if A.termMatrix == [[' ']] or B.termMatrix == [[' ']]:
        return False
    tempa, tempb = multivariable_polynomial.Polynomial.combine_variables(A, B)
    a = tempa.termMatrix
    b = tempb.termMatrix
    res = True
    for i in range(1, len(a[1])):
        if a[1][i] > b[1][i]:
            res = False
    return res


def monomialDivide(A, B):
    A, B = multivariable_polynomial.Polynomial.combine_variables(A, B)
    res = A
    res.termMatrix[1][0] = A.termMatrix[1][0] / B.termMatrix[1][0]
    for i in range(1, len(res.termMatrix[0])):
        for j in range(1, len(res.termMatrix)):
            res.termMatrix[j][i] -= B.termMatrix[j][i]
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
    p = multivariable_polynomial.Polynomial([t[:] for t in input_poly.termMatrix[:]])
    r = multivariable_polynomial.Polynomial(0)
    while p != multivariable_polynomial.Polynomial(0):
        i = 0
        division_occured = False
        while i < len(others) and division_occured == False:
            if divides(others[i], p):
                a[i] += monomialDivide(p.LT(), others[i].LT())
                p -= monomialDivide(p.LT(), others[i].LT())*others[i]
                division_occured = True
            else:
                i += 1
        if division_occured == False:
            p_LT = p.LT()
            r += p_LT
            p -= p.LT()
    for poly in a:
        poly.termMatrix = input_poly.mod_poly(poly.termMatrix)
    r.termMatrix = input_poly.mod_poly(r.termMatrix)
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
