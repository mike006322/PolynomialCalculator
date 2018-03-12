from parser import parse_poly as parse
from orderings import order_lex as order
from CollectLikeTerms import collectLikeTerms

class Polynomial:
    
    def __init__(self, poly_string):
        self.termMatrix = parse(poly_string)
        self.termMatrix = collectLikeTerms(self.termMatrix)
        self.termMatrix = order(self.termMatrix)
        #what about zero polynomial?
    
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
        return Polynomial.clean([self.termMatrix[0], self.termMatrix[1]])
    
    def __repr__(self):
        pass
    
    def __call__(self, ):
        pass
    
    def __add__(self, other):
        pass
    
    def __sub__(self, other):
        pass
    
    def __mul__(self, other):
        pass
    
    def derivative(self, var):
        pass
    
    def __str__(self):
        pass
    
    def __truediv__(self, other):
        pass
    
    def GCD(self, other):
        pass

if __name__ == '__main__':
    s = 'yx^2+yx+x+x+4+z'
    p = Polynomial(s)
    print(s)
    print(p.LT())