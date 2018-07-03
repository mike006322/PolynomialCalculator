from poly_parser import parse_poly as parse
from orderings import order_lex as order
from CollectLikeTerms import collectLikeTerms

class InputError(Exception):
    
    def __init__(self):
        print("Polynomial input needs to be similar to following example: 'x^2+2xy^3+4'")
        print("Alternatively, try a term matrix in form [[' ', 'x', 'y'], [1.0, 2, 0], [2.0, 1, 3], [4.0, 0, 0]]")
        

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
            self.termMatrix = collectLikeTerms(self.termMatrix)
            self.termMatrix = order(self.termMatrix)
        else:
            raise InputError
        
    @staticmethod
    def clean(termMatrix):
        #removes extra variables
        res = termMatrix
        j = 0
        while j < len(termMatrix[0]):
            for i in range(1, len(res[0])):
                allZero = True
                for term in res[1:]:
                    if term[i] != 0:
                        allZero = False
                if allZero:
                    if i < len(res[0])-1:
                        res = [x[0:i] + x[i+1:] for x in res] 
                    else:
                        res = [x[0:i] for x in res]
                    break
            j += 1
        return res
    
    @staticmethod    
    def combine_variables(A, B):
        var_set = set(A.termMatrix[0]).union(set(B.termMatrix[0]))
        res = [sorted(list(var_set))]
        for var in res[0]:
            if var not in A.termMatrix[0]:
                A.termMatrix[0].append(var)
                for term in A.termMatrix[1:]:
                    term.append(0)
            if var not in B.termMatrix[0]:
                B.termMatrix[0].append(var)
                for term in B.termMatrix[1:]:
                    term.append(0)
        A.termMatrix = order(A.termMatrix)
        B.termMatrix = order(B.termMatrix)
        return A, B
    
    def LT(self):
        #leading term
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
    
    def __repr__(self):
        return "Polynomial" + str(self.termMatrix)
    
    def __call__(self, **kwargs):
        #input is variables as key word arguments, e.g. "x = 2, y = 3"
        res = 0
        for term in self.termMatrix[1:]:
            to_add = term[0]
            for i in range(1, len(term)):
                to_add *= kwargs[self.termMatrix[0][i]] ** term[i]
            res += to_add
        return res
    
    def __add__(self, other):
        if len(self.termMatrix) == 1:
            self.termMatrix = [[' '], [0]]
        if len(other.termMatrix) == 1:
            other.termMatrix = [[' '], [0]]
        var_set = set(self.termMatrix[0]).union(set(other.termMatrix[0]))
        res = [sorted(list(var_set))]
        #first add variables to both, then order both, then combine both
        self, other = Polynomial.combine_variables(self, other)
        res += self.termMatrix[1:]
        res += other.termMatrix[1:]
        res = collectLikeTerms(res)
        res = order(res)
        return Polynomial(res)
    
    def __sub__(self, other):
        if self == other:
            return Polynomial([[' ']])
        for term in other.termMatrix[1:]:
            term[0] = -term[0]
        return self + other
    
    def __mul__(self, other):
        #first add variables and order
        self, other = Polynomial.combine_variables(self, other)
        res = [self.termMatrix[0]]
        #then distribute that multiplication
        for term in self.termMatrix[1:]:
            for other_term in other.termMatrix[1:]:
                product = []
                product.append(term[0]*other_term[0])
                for i in range(1, len(term)):
                    product.append(term[i] + other_term[i])
                res.append(product)
        res = collectLikeTerms(res)
        res = order(res)
        return Polynomial(res)
    
    def derivative(self, var):
        pass
    
    def __str__(self):
        res = ""
        if len(self.termMatrix) == 1:
            return "0"
        for term in self.termMatrix[1:]:
            #display coefficient if it's not 1
            if term[0] != 1:
                res += str(term[0])
            #display coefficient if there are no other exponents
            if len(term) == 1:
                res += str(term[0])
            #display coefficient if it's 1 and all exponents are 0
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
    
    @staticmethod    
    def divides(A, B):
        #returns True if LT(a) has exponents all less than LT(b)
        if A.termMatrix == [[' ']] or B.termMatrix == [[' ']]:
            return False
        A, B = Polynomial.combine_variables(A, B)
        a = A.termMatrix
        b = B.termMatrix
        res = True
        for i in range(1, len(a[1])):
            if a[1][i] > b[1][i]:
                res = False
        A.termMatrix = collectLikeTerms(A.termMatrix)
        B.termMatrix = collectLikeTerms(B.termMatrix)
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
    
    def divide(self, *others):
        #others is an ordered tuple of functions
        a = []
        for i in range(len(others)):
            a.append(Polynomial(0))
        p = self
        r = Polynomial(0)
        while p.termMatrix != [[' ']]:
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
    
    def divide_string(self, *others):
        a, r = self.divide(*others)
        res = str(self) + ' = '
        for i in range(len(a)):
            res += '(' + str(a[i]) + ')' + ' * ' + '(' + str(others[i]) + ')' + ' + '
        if res.endswith(" + "):
            res = res[:-3]
        res += ', remainder = ' + str(r)
        return res

if __name__ == '__main__':
    s = 'x^2y + xy^2 + y^2'
    t = 'xy - 1'
    e = 'y^2 - 1'
    S = Polynomial(s)
    T = Polynomial(t)
    E = Polynomial(e)
    print(S.divide_string(T, E))
