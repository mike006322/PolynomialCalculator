from poly_parser import parse_poly as parse
from orderings import order_lex as order
from collect_like_terms import collect_like_terms
from division_algorithm import division_algorithm
import formulas


class InputError(Exception):

    def __init__(self):
        print("Polynomial input needs to be similar to following example: 'x^2+2xy^3+4'")
        print("Alternatively, try a term matrix in form [[' ', 'x', 'y'], [1.0, 2, 0], [2.0, 1, 3], [4.0, 0, 0]]")


class NonFactor(Exception):

    def __init__(self, q, p):
        super().__init__("{} does not divide {}".format(q, p))


class Polynomial:

    def __init__(self, poly, char=0):
        if poly == 0:
            self.term_matrix = [[' ']]
            self.field_characteristic = char
        elif isinstance(poly, (int, float, complex)) and poly != 0:
            self.term_matrix = [[' '], [poly]]
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
        return Polynomial([t[:] for t in self.term_matrix])

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
        return formulas.solve(self)

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
            self.term_matrix = [[' '], [0]]
        self.term_matrix = order(self.term_matrix)
        res = [[], []]
        for variable in self.term_matrix[0]:
            res[0].append(variable)
        for coefficient in self.term_matrix[1]:
            res[1].append(coefficient)
        Polynomial.clean(res)
        return Polynomial(res)

    def __repr__(self):
        return "Polynomial({})".format(self.term_matrix)

    def __str__(self):
        res = ""
        if len(self.term_matrix) == 1:
            return "0"
        for term in self.term_matrix[1:]:
            # display coefficient if it's not 1
            if term[0] != 1 and len(self.term_matrix[0]) > 1:
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
                self.term_matrix = [[' '], [0]]
            if len(other.term_matrix) == 1:
                other.term_matrix = [[' '], [0]]
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
            return self + Polynomial(other)
        return Polynomial(res)

    __radd__ = __add__

    def __sub__(self, other):
        if type(other) == Polynomial:
            if self == other:
                return Polynomial([[' ']])
            for term in other.term_matrix[1:]:
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
            res = [self_copy.term_matrix[0]]
            # then distribute that multiplication
            for term in self_copy.term_matrix[1:]:
                for other_term in other_copy.term_matrix[1:]:
                    product = []
                    product.append(term[0]*other_term[0])
                    for i in range(1, len(term)):
                        product.append(term[i] + other_term[i])
                    res.append(product)
            res = collect_like_terms(res)
            res = order(res)
        else:
            return self * Polynomial(other)
        res = self.mod_char(res)
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
            return self / Polynomial(other)

    def __rtruediv__(self, other):
        return Polynomial(other) / self

    def __mod__(self, other):
        """
        returns the remainder of self/other
        """
        if type(other) == Polynomial:
            return division_algorithm(self, other)[1]
        else:
            return self % Polynomial(other)

    def __eq__(self, other):
        if type(other) == Polynomial:
            if self.term_matrix == other.term_matrix:
                return True
            else:
                return False
        else:
            return self == Polynomial(other)
