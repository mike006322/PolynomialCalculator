from core.poly_parser import parse_poly as parse
from core.orderings import order_lex as order
from core.orderings import graded_lex as graded_order
from core.collect_like_terms import collect_like_terms
from core.formulas import *


class InputError(Exception):

    def __init__(self):
        print("Polynomial input needs to be similar to following example: 'x^2+2xy^3+4'")
        print("Alternatively, try a term matrix in form [['constant, 'x', 'y'], [1.0, 2, 0], [2.0, 1, 3], [4.0, 0, 0]]")


class NonFactor(Exception):

    def __init__(self, q, p):
        super().__init__("{} does not divide {}".format(q, p))


class Polynomial:

    def __init__(self, poly, char=0):
        if poly == 0:
            self.term_matrix = [['constant']]
            self.field_characteristic = char
        elif isinstance(poly, (int, float, complex)) and poly != 0:
            self.term_matrix = [['constant'], [poly]]
            self.field_characteristic = char
        elif type(poly) == list:
            self.term_matrix = poly
            self.field_characteristic = char
        elif type(poly) == str:
            self.term_matrix = parse(poly)
            self.term_matrix = collect_like_terms(self.term_matrix)
            self.term_matrix = order(self.term_matrix)
            self.field_characteristic = char
        else:
            raise InputError
        self.term_matrix = self.mod_char(self.term_matrix)

    def copy(self):
        return Polynomial([t[:] for t in self.term_matrix], self.field_characteristic)

    def mod_char(self, term_matrix):
        """
        mods the term_matrix by the field characteristic if it's greater than 0
        """
        if self.field_characteristic > 0:
            term_matrix_iter = iter(term_matrix)
            next(term_matrix_iter)
            for term in term_matrix_iter:
                term[0] %= self.field_characteristic
            term_matrix = collect_like_terms(term_matrix)
            return term_matrix
        else:
            return term_matrix

    def __iter__(self):
        """
        yields terms of the polynomial as individual polynomials
        """
        terms = iter(self.term_matrix)
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
        return solve(self)

    def degree(self):
        """
        returns degree of polynomial if single variable
        returns highest power if multivariable
        """
        if len(self.term_matrix[0]) == 1:
            return 0
        else:
            t = self.copy()
            t.term_matrix = graded_order(t.term_matrix)
            return sum(t.term_matrix[1][1:])

    def variables(self):
        """
        returns the variables of the polynomial as a set
        """
        res = set(self.term_matrix[0])
        res.remove('constant')
        return res

    def number_of_variables(self):
        """
        returns the number of variables in the polynomial
        """
        return len(self.variables())

    @staticmethod
    def clean(term_matrix):
        """
        input is polynomial in term_matrix
        returns term_matrix with minimum number of variables
        """
        res = term_matrix
        j = 0
        while j < len(term_matrix[0]):
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
    def combine_variables(a, b):
        """
        input is two polynomials
        returns two polynomials with term_matricies that have same variables
        """
        a = a.copy()
        b = b.copy()
        var_set = set(a.term_matrix[0]).union(set(b.term_matrix[0]))
        res = [sorted(list(var_set))]
        for var in res[0]:
            if var not in a.term_matrix[0]:
                a.term_matrix[0].append(var)
                for term in a.term_matrix[1:]:
                    term.append(0)
            if var not in b.term_matrix[0]:
                b.term_matrix[0].append(var)
                for term in b.term_matrix[1:]:
                    term.append(0)
        a.term_matrix = order(a.term_matrix)
        b.term_matrix = order(b.term_matrix)
        return a, b

    def LT(self):
        """
        returns the leading term of the polynomial
        """
        if len(self.term_matrix) == 1:
            return Polynomial(0, self.field_characteristic)
        self.term_matrix = order(self.term_matrix)
        res = [[], []]
        for variable in self.term_matrix[0]:
            res[0].append(variable)
        for coefficient in self.term_matrix[1]:
            res[1].append(coefficient)
        Polynomial.clean(res)
        return Polynomial(res, self.field_characteristic)

    def LM(self):
        """
        returns leading monomial
        """
        res = self.LT()
        if res != 0:
            res.term_matrix[1][0] /= res.term_matrix[1][0]
        return res

    def isolate(self, variable):
        """
        isolates a single variable, not necessarily in self
        returns a polynomial of one variable with polynomial constant terms
        """
        poly = self.copy()
        if variable in poly.variables():
            i = poly.term_matrix[0].index(variable)
        else:
            return self
        if i != len(poly.variables()):
            remaining_vars = poly.term_matrix[0][:i] + poly.term_matrix[0][i+1:]
        else:
            remaining_vars = poly.term_matrix[0][:i]
        res = Polynomial([['constant', variable]], poly.field_characteristic)
        for term in poly.term_matrix[1:]:
            variable_power = term.pop(i)
            res.term_matrix += [[Polynomial(Polynomial.clean([remaining_vars, term])), variable_power]]
        res.term_matrix = collect_like_terms(res.term_matrix)
        return res

    def __repr__(self):
        return "Polynomial({})".format(self.term_matrix)

    def __str__(self):
        res = ""
        if len(self.term_matrix) == 1:
            return "0"
        for term in self.term_matrix[1:]:
            # display coefficient if it's not 1
            if term[0] != 1 and len(self.term_matrix[0]) > 1:
                if type(term[0]) == Polynomial:
                    res += '(' + str(term[0]) + ')'
                else:
                    res += str(term[0])
            # display coefficient if there are no other exponents
            if len(term) == 1:
                res += str(term[0])
            # display coefficient if it's 1 and all exponents are 0
            if len(term) > 1:
                if term[0] == 1 and all(x == 0 for x in term[1:]):
                    res += str(term[0])
            for i in range(1, len(self.term_matrix[0])):
                if term[i] != 0:
                    res += self.term_matrix[0][i]
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
        for term in self.term_matrix[1:]:
            to_add = term[0]
            for i in range(1, len(term)):
                to_add *= kwargs[self.term_matrix[0][i]] ** term[i]
            res += to_add
        return res

    def __add__(self, other):
        if type(other) == Polynomial:
            if len(self.term_matrix) == 1:
                self.term_matrix = [['constant'], [0]]
            if len(other.term_matrix) == 1:
                other.term_matrix = [['constant'], [0]]
            var_set = set(self.term_matrix[0]).union(set(other.term_matrix[0]))
            res = [sorted(list(var_set))]
            # first add variables to both, then order both, then combine both
            self_copy, other_copy = Polynomial.combine_variables(self, other)
            res += self_copy.term_matrix[1:]
            res += other_copy.term_matrix[1:]
            res = collect_like_terms(res)
            res = order(res)
            res = self.mod_char(res)
        else:
            return self + Polynomial(other, self.field_characteristic)
        return Polynomial(res, self.field_characteristic)

    __radd__ = __add__

    def __sub__(self, other):
        if type(other) == Polynomial:
            if self == other:
                return Polynomial([['constant']], self.field_characteristic)
            for term in other.term_matrix[1:]:
                term[0] = -term[0]
        else:
            return self - Polynomial(other, self.field_characteristic)
        return self + other

    def __rsub__(self, other):
        return Polynomial(other) - self

    def __mul__(self, other):
        if type(other) == Polynomial:
            # first add variables and order
            self_copy, other_copy = Polynomial.combine_variables(self, other)
            res = [self_copy.term_matrix[0]]
            # then distribute that multiplication
            for term in self_copy.term_matrix[1:]:
                for other_term in other_copy.term_matrix[1:]:
                    product = list()
                    product.append(term[0]*other_term[0])
                    for i in range(1, len(term)):
                        product.append(term[i] + other_term[i])
                    res.append(product)
            res = collect_like_terms(res)
            res = order(res)
        else:
            return self * Polynomial(other, self.field_characteristic)
        res = self.mod_char(res)
        return Polynomial(res, self.field_characteristic)

    __rmul__ = __mul__

    def __pow__(self, other):
        """
        power must be positive integer
        """
        if other == 0:
            return Polynomial('1', self.field_characteristic)
        res = self.copy()
        n = other
        while n > 1:
            res *= self
            n -= 1
        return res

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
            div_alg_results = division_algorithm(self, other)
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
            return self / Polynomial(other, self.field_characteristic)

    def __rtruediv__(self, other):
        return Polynomial(other) / self

    def __mod__(self, other):
        """
        returns the remainder of self/other
        """
        if type(other) == Polynomial:
            return division_algorithm(self, other)[1]
        else:
            return self % Polynomial(other, self.field_characteristic)

    def __rmod__(self, other):
        """
        returns the remainder of other/self
        """
        # __rmod__ cannot override the string's LHS __mod__ operator, see bug at: https://bugs.python.org/issue28598
        pass

    def __eq__(self, other):
        if type(other) == Polynomial:
            if self.term_matrix == other.term_matrix:
                return True
            else:
                return False
        else:
            return self == Polynomial(other, self.field_characteristic)


def divides(a, b):
    """
    returns True if LT(a) has exponents all less than LT(b)
    """
    if a.term_matrix == [['constant']] or b.term_matrix == [['constant']]:
        return False
    a, b = Polynomial.combine_variables(a, b)
    a = a.term_matrix
    b = b.term_matrix
    res = True
    for i in range(1, len(a[1])):
        if a[1][i] > b[1][i]:
            res = False
    return res


def monomial_divide(a, b):
    a, b = Polynomial.combine_variables(a, b)
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
        a.append(Polynomial(0, input_poly.field_characteristic))
    p = input_poly.copy()
    r = Polynomial(0, input_poly.field_characteristic)
    while p != Polynomial(0):
        i = 0
        division_occurred = False
        while i < len(others) and not division_occurred:
            if divides(others[i], p):
                a[i] += monomial_divide(p.LT(), others[i].LT())
                p -= monomial_divide(p.LT(), others[i].LT()) * others[i]
                division_occurred = True
            else:
                i += 1
        if not division_occurred:
            p_LT = p.LT()
            r += p_LT
            p -= p.LT()
    for poly in a:
        poly.term_matrix = input_poly.mod_char(poly.term_matrix)
    r.term_matrix = input_poly.mod_char(r.term_matrix)
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


def gcd(a, b):
    """
    input is polynomials
    output the greatest common divisor
    if input is multivariate, recurse on the variables solving one at a time
    i.e. if a, b in R[x_1, x_2], first do a, b in R[x_1][x_2]
    # multivariate currently only works for monomials
    """
    a = a.copy()
    b = b.copy()
    if a.number_of_variables() <= 1 and b.number_of_variables() <= 1:
        return gcd_singlevariate(a, b)
    if len(a.term_matrix) > 2 or len(b.term_matrix) > 2:
        raise NotImplemented
    res = gcd_singlevariate(Polynomial(a.term_matrix[1][0]), Polynomial(b.term_matrix[1][0]))
    for variable in a.variables().union(b.variables()):
        isolated_a = a.isolate(variable)
        isolated_b = b.isolate(variable)
        res *= Polynomial(variable)**min(isolated_a.term_matrix[1][1], isolated_b.term_matrix[1][1])
    return res


def gcd_singlevariate(a, b):
    """
    input is polynomials of one variable
    returns greatest common divisor
    alternative/faster algorithm to implement:
    https://en.wikipedia.org/wiki/Polynomial_greatest_common_divisor#B%C3%A9zout's_identity_and_extended_GCD_algorithm
    """
    a = a.copy()
    b = b.copy()
    if a.degree() == b.degree():
        if a == b:
            return a
    if a.degree() >= b.degree():
        r = a % b
        while r != 0:
            a = b
            b = r
            r = a % b
        return b
    else:
        a, b = b, a
        return gcd(a, b)


def lcm(a, b):
    """
    returns least common multiple of two polynomials
    """
    return a*b/gcd(a, b)
