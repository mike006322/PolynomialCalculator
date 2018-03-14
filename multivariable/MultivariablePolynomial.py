from parser import parse_poly as parse
from orderings import order_lex as order
from CollectLikeTerms import collectLikeTerms

class Polynomial:
    
    def __init__(self, poly):
        if type(poly) == list:
            self.termMatrix = poly
        if type(poly) == str:
            self.termMatrix = parse(poly)
            self.termMatrix = collectLikeTerms(self.termMatrix)
            self.termMatrix = order(self.termMatrix)
        
    
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
            
    
    def LT(self):
        #leading term
        self.termMatrix = order(self.termMatrix)
        return Polynomial(Polynomial.clean([self.termMatrix[0], self.termMatrix[1]]))
    
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
        var_set = set(self.termMatrix[0]).union(set(other.termMatrix[0]))
        res = [sorted(list(var_set))]
        #first add variables to both, then order both, then combine both
        for var in res[0]:
            if var not in self.termMatrix[0]:
                self.termMatrix[0].append(var)
                for term in self.termMatrix[1:]:
                    term.append(0)
            if var not in other.termMatrix[0]:
                other.termMatrix[0].append(var)
                for term in other.termMatrix[1:]:
                    term.append(0)
        self.termMatrix = order(self.termMatrix)
        other.termMatrix = order(other.termMatrix)
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
        var_set = set(self.termMatrix[0]).union(set(other.termMatrix[0]))
        res = [sorted(list(var_set))]
        for var in res[0]:
            if var not in self.termMatrix[0]:
                self.termMatrix[0].append(var)
                for term in self.termMatrix[1:]:
                    term.append(0)
            if var not in other.termMatrix[0]:
                other.termMatrix[0].append(var)
                for term in other.termMatrix[1:]:
                    term.append(0)
        self.termMatrix = order(self.termMatrix)
        other.termMatrix = order(other.termMatrix)
        #then define multiplication of single terms
        def mul_terms(a, b):
            product = []
            product.append(a[0]*b[0])
            for i in range(1, len(a)):
                product.append(a[i] + b[i])
            return product
        #then distribute that multiplication
        for term in self.termMatrix[1:]:
            for other_term in other.termMatrix[1:]:
                res.append(mul_terms(term, other_term))
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
            if term[0] != 1:
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
    
    def __truediv__(self, other):
        pass
    
    def GCD(self, other):
        pass

if __name__ == '__main__':
    s = 'x^2+2'
    t = 'y^3+x^2+3'
    p = Polynomial(s)
    q = Polynomial(t)
    print(s)
    print(t)
    print(p)