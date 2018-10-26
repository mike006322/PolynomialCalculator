from poly_parser import parse_poly as parse
from orderings import order_lex as order
from collect_like_terms import collect_like_terms
import formulas

class InputError(Exception):

    def __init__(self):
        print("Polynomial input needs to be similar to following example: 'x^2+2xy^3+4'")
        print("Alternatively, try a term matrix in form [[' ', 'x', 'y'], [1.0, 2, 0], [2.0, 1, 3], [4.0, 0, 0]]")


class NonFactor(Exception):

    def __init__(self, q, p):
        super().__init__("{} does not divide {}".format(q, p))

class Polynomial:

    def __init__(self, poly):
        if poly == 0:
            self.termMatrix = [[' ']]
        elif isinstance(poly, (int, float, complex)) and poly != 0:
            self.termMatrix = [[' '], [poly]]
        elif type(poly) == list:
            self.termMatrix = poly
        elif type(poly) == str:
            self.termMatrix = parse(poly)
            self.termMatrix = collect_like_terms(self.termMatrix)
            self.termMatrix = order(self.termMatrix)
        else:
            raise InputError

    def __iter__(self):
        """
        yields terms of the polynomial as individual polynomials
        """
        self.termMatrix
        terms = iter(self.termMatrix)
        variables = next(terms)
        for term in terms:
            p = [variables, term]
            yield Polynomial(collect_like_terms(p))

    def derivative(self, var):
        """
        returns the derivative with respect to var
        """
        return solve(self)

    def solve(self):
        """
        returns zeros of the polynomial if able
        """
        return formulas.solve(self)

    @staticmethod
    def clean(termMatrix):
        """
        input is polynomial in termMatrix
        returns termMatrix with minimum number of variables
        """
        res = termMatrix
        j = 0
        while j < len(termMatrix[0]):
            for i in range(1, len(res[0])):
                all_zero = True
                for term in res[1:]:
                    if term[i] != 0:
                        all_zero = False
                if all_zero:
                    if i < len(res[0])-1:
                        res = [x[0:i] + x[i+1:] for x in res]
                    else:
                        res = [x[0:i] for x in res]
                    break
            j += 1
        return res

    @staticmethod
    def combine_variables(A, B):
        """
        input is two polynomials
        returns two polynomials with termMatricies that have same variables
        """
        a = Polynomial(A.termMatrix[:])
        b = Polynomial(B.termMatrix[:])
        var_set = set(a.termMatrix[0]).union(set(b.termMatrix[0]))
        res = [sorted(list(var_set))]
        for var in res[0]:
            if var not in a.termMatrix[0]:
                a.termMatrix[0].append(var)
                for term in a.termMatrix[1:]:
                    term.append(0)
            if var not in b.termMatrix[0]:
                b.termMatrix[0].append(var)
                for term in b.termMatrix[1:]:
                    term.append(0)
        a.termMatrix = order(a.termMatrix)
        b.termMatrix = order(b.termMatrix)
        return a, b

    def LT(self):
        """
        returns the leading term of the polynomial
        """
        if len(self.termMatrix) == 1:
            self.termMatrix = [[' '], [0]]
        self.termMatrix = order(self.termMatrix)
        res = [[], []]
        for i in range(len(self.termMatrix[0])):
            res[0].append(self.termMatrix[0][i])
        for i in range(len(self.termMatrix[1])):
            res[1].append(self.termMatrix[1][i])
        Polynomial.clean(res)
        return Polynomial(res)

    @staticmethod
    def divides(A, B):
        """
        returns True if LT(a) has exponents all less than LT(b)
        """
        if A.termMatrix == [[' ']] or B.termMatrix == [[' ']]:
            return False
        tempa, tempb = Polynomial.combine_variables(A, B)
        a = tempa.termMatrix
        b = tempb.termMatrix
        res = True
        for i in range(1, len(a[1])):
            if a[1][i] > b[1][i]:
                res = False
        return res

    @staticmethod
    def monomialDivide(A, B):
        A, B = Polynomial.combine_variables(A, B)
        res = A
        res.termMatrix[1][0] = A.termMatrix[1][0] / B.termMatrix[1][0]
        for i in range(1, len(res.termMatrix[0])):
            for j in range(1, len(res.termMatrix)):
                res.termMatrix[j][i] -= B.termMatrix[j][i]
        return res

    def division_algorithm(self, *others):
        """
        input is polynomial/s
        output is self divided by other polynomial/s and a remainder as Polynomial classes
        """
        # others is an ordered tuple of functions
        a = []
        for i in range(len(others)):
            a.append(Polynomial(0))
        p = self
        r = Polynomial(0)
        while p != Polynomial(0):
            i = 0
            division_occured = False
            while i < len(others) and division_occured == False:
                if Polynomial.divides(others[i], p):
                    a[i] += Polynomial.monomialDivide(p.LT(), others[i].LT())
                    p -= Polynomial.monomialDivide(p.LT(), others[i].LT())*others[i]
                    division_occured = True
                else:
                    i += 1
            if division_occured == False:
                p_LT = p.LT()
                r += p_LT
                p -= p.LT()
        return a, r

    def division_string(self, *others):
        """
        input is polynomial/s
        output is string "[self] = ([divisor])*([other polynomial/s]) + ([remainder:]) remainder"
        """
        a, r = self.division_algorithm(*others)
        res = str(self) + ' = '
        for i in range(len(a)):
            res += '(' + str(a[i]) + ')' + '*' + '(' + str(others[i]) + ')' + ' + '
        if res.endswith(" + "):
            res = res[:-3]
        res += ' + (remainder:) ' + str(r)
        return res

    def __repr__(self):
        return "Polynomial({})".format(self.termMatrix)

    def __str__(self):
        res = ""
        if len(self.termMatrix) == 1:
            return "0"
        for term in self.termMatrix[1:]:
            # display coefficient if it's not 1
            if term[0] != 1 and len(self.termMatrix[0]) > 1:
                res += str(term[0])
            # display coefficient if there are no other exponents
            if len(term) == 1:
                res += str(term[0])
            # display coefficient if it's 1 and all exponents are 0
            if len(term) > 1:
                if term[0] == 1 and all(x == 0 for x in term[1:]):
                    res += str(term[0])
            for i in range(1, len(self.termMatrix[0])):
                if term[i] != 0:
                    res += self.termMatrix[0][i]
                    if term[i] != 1:
                        res += "^" + str(term[i])
            res += " + "
        if res.endswith(" + "):
            res = res[:-3]
        return res

    def __call__(self, **kwargs):
        """
        input is variables as key word arguments, e.g. "x = 2, y = 3"
        """
        res = 0
        for term in self.termMatrix[1:]:
            to_add = term[0]
            for i in range(1, len(term)):
                to_add *= kwargs[self.termMatrix[0][i]] ** term[i]
            res += to_add
        return res

    def __add__(self, other):
        if type(other) == Polynomial:
            if len(self.termMatrix) == 1:
                self.termMatrix = [[' '], [0]]
            if len(other.termMatrix) == 1:
                other.termMatrix = [[' '], [0]]
            var_set = set(self.termMatrix[0]).union(set(other.termMatrix[0]))
            res = [sorted(list(var_set))]
            # first add variables to both, then order both, then combine both
            self_copy, other_copy = Polynomial.combine_variables(self, other)
            res += self_copy.termMatrix[1:]
            res += other_copy.termMatrix[1:]
            res = collect_like_terms(res)
            res = order(res)
        else:
            return self + Polynomial(other)
        return Polynomial(res)

    __radd__ = __add__

    def __sub__(self, other):
        if type(other) == Polynomial:
            if self == other:
                return Polynomial([[' ']])
            for term in other.termMatrix[1:]:
                term[0] = -term[0]
        else:
            return self - Polynomial(other)
        return self + other

    def __rsub__(self, other):
        return Polynomial(other) - self

    def __mul__(self, other):
        if type(other) == Polynomial:
            # first add variables and order
            self_copy, other_copy = Polynomial.combine_variables(self, other)
            res = [self_copy.termMatrix[0]]
            # then distribute that multiplication
            for term in self_copy.termMatrix[1:]:
                for other_term in other_copy.termMatrix[1:]:
                    product = []
                    product.append(term[0]*other_term[0])
                    for i in range(1, len(term)):
                        product.append(term[i] + other_term[i])
                    res.append(product)
            res = collect_like_terms(res)
            res = order(res)
        else:
            return self * Polynomial(other)
        return Polynomial(res)

    __rmul__ = __mul__

    def __truediv__(self, other):
        """
        returns the quotient using the polynomial division algorithm
        raises error if the denominator is not a factor of the numerator
        """
        if type(other) == Polynomial:
            if other == 1:
                return self
            if other == 0:
                raise ZeroDivisionError
            div_alg_results = self.division_algorithm(other)
            if div_alg_results[1] != 0:
                raise NonFactor(other, self)
            if self == div_alg_results[1]:
                return 0
            else:
                res = 1
                for factor in div_alg_results[0]:
                    res *= factor
                return res
        else:
            return self / Polynomial(other)

    def __rtruediv__(self, other):
        return Polynomial(other) / self

    def __eq__(self, other):
        if type(other) == Polynomial:
            if self.termMatrix == other.termMatrix:
                return True
            else:
                return False
        else:
            return self == Polynomial(other)


if __name__ == '__main__':
    s = 'x^2y + xy^2 + y^2'
    t = 'xy - 1'
    e = 'y^2 - 1'
    S = Polynomial(s)
    T = Polynomial(t)
    E = Polynomial(e)
    poly1 = 'x^2-4x+4'
    poly2 = 'x-2'
    Poly1 = Polynomial(poly1)
    Poly2 = Polynomial(poly2)
    print(S.division_string(T, E))
    print(S.division_algorithm(T, E))
    #print(S.division_algorithm(Polynomial('x'),Polynomial('y')))
    print(S.division_string(Polynomial('x'),Polynomial('y')))
    #print(Polynomial('x').division_algorithm(Polynomial('y')))
    #print(Polynomial('x^2-1').division_string(Polynomial('x+1')))
    #print(Polynomial('x^2-1')/'x+1')
    #print('x^2-1'/Polynomial('x+1'))
    print(Polynomial('x+5'))
    print(Poly1.division_string(Poly2))
    print(Polynomial('3x^2 + x + 5').termMatrix)
    print(T.division_string(E))
    print(T.division_algorithm(E)[1])
    print(T/E)

