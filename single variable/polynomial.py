#Polynomal class for polynomials of one variable (x)
#Python 3 for division to work properly (truediv method overload)

class Polynomial:
    
    def __init__(self, *coefficients):
        # input: coefficients are in the form a_n, ...a_1, a_0
        # for reasons of efficiency we save the coefficients in reverse order,
        # i.e. a_0, a_1, ... a_n
        # coefficients are stored in the object as a tuple
        self.coefficients = coefficients[::-1]
        #LT = leading term in form (coefficient, degree)
        
      
    # method to return the canonical string representation of a polynomial
    def __repr__(self):
        return "Polynomial" + str(self.coefficients)
        
    def __call__(self, x):    
        res = 0
        for index, coeff in enumerate(self.coefficients):
            res += coeff * x** index
        return res

    def degree(self):
        return len(self.coefficients) - 1
        #this means that a_n must be non-zero and there must be a value for all n
        
    @staticmethod
    def zip_longest(iter1, iter2, fillchar=0):  
    # used to zip together coefficients 
    # pairing 0 with the coefficients of highest degree if the counterpart doesn't have as high of a degree.
        for i in range(max(len(iter1), len(iter2))):
            if i >= len(iter1):
                yield (fillchar, iter2[i])
            elif i >= len(iter2):
                yield (iter1[i], fillchar)
            else:
                yield (iter1[i], iter2[i])
            i += 1  
            
    def __add__(self, other):
        c1 = self.coefficients
        c2 = other.coefficients
        res = [sum(t) for t in Polynomial.zip_longest(c1, c2)]
        return Polynomial(*res[::-1])

    def __sub__(self, other):
        c1 = self.coefficients
        c2 = other.coefficients
        res = [t1-t2 for t1, t2 in Polynomial.zip_longest(c1, c2)]
        while res[-1] == 0:
            res = res[:-1]
            if res == []:
                break
        return Polynomial(*res[::-1])
        
    def __mul__(self, other):
        c1 = self.coefficients
        c2 = other.coefficients
        res = [0]*(len(c1)+len(c2)-1)
        for o1,i1 in enumerate(c1):
            for o2,i2 in enumerate(c2):
                res[o1+o2] += i1*i2
        return Polynomial(*res[::-1])
        
    def derivative(self):
        derived_coeffs = []
        exponent = 1
        for i in range(1, len(self.coefficients)):
            derived_coeffs.append(self.coefficients[i] * exponent)
            exponent += 1
        return Polynomial(*derived_coeffs)
        
    def __str__(self):
        res = ""
        if len(self.coefficients) == 0:
            res = "0"
        for i in range(len(self.coefficients)-1, -1, -1):
            if self.coefficients[i] == 1 and str(i) == "1":
                res +=  "x" + " + "
            elif self.coefficients[i] == 1 and str(i) != "1":
                res +=  "x^" + str(i) + " + "
            elif self.coefficients[i] != 0 and str(i) == "0":
                res +=  str(self.coefficients[i]) + " + "
            elif self.coefficients[i] != 0 and str(i) == "1":
                res +=  str(self.coefficients[i]) + "x" + " + "
            elif self.coefficients[i] != 0 and str(i) != "0" and str(i) != "1":
                res +=  str(self.coefficients[i]) + "x^" + str(i) + " + "
        if res.endswith(" + "):
            res = res[:-3]
        return res
        
    def LT(self):
        if len(self.coefficients) >= 1:
            return Polynomial(self.coefficients[-1],*[0]*(len(self.coefficients)-1)) 
        else: 
            return Polynomial()
     
      
    def __truediv__(self, other):
        q = Polynomial(0)
        r = self
        while r != 0 and other.LT().degree() <= r.LT().degree(): 
            v = other.LT().coefficients[-1]
            ltrDivLtself = Polynomial(r.LT().coefficients[-1]/other.LT().coefficients[-1], *[0]*(r.degree()-other.degree())) #LT(r)/LT(g)
            q = q + ltrDivLtself
            r = r - ltrDivLtself*other
        return q, r
        
    def GCD(self, other):
        h = self
        s = other
        while len(s.coefficients) != 0: # s != 0
            rem = (h/s)[1]
            h = s
            s = rem
        return h

if __name__ == "__main__":
    p = Polynomial(1, 2, 3, 4, 5)
    print(p, " 'print(p)'")
    p_der = p.derivative()
    print(p_der, " 'print(p_der)'")
    print(p.coefficients, " 'print(p.coefficients)'")
    print(p-p, " 'print(p-p)'")
    print(p/p, " 'print(p/p)'")
    print(Polynomial(1,0,-1)/Polynomial(1,-1), " 'print(Polynomial(1,0,-1)/Polynomial(1,-1))'")
    print(Polynomial(1,0,-1), " 'print(Polynomial(1,0,-1))'")
    print(Polynomial.GCD(Polynomial(1,0,-1), Polynomial(1,-1)))
    
'''
import numpy as np
import matplotlib.pyplot as plt
X = np.linspace(-3, 3, 50, endpoint=True)
F1 = p1(X)
F2 = p2(X)
F_sum = p_sum(X)
F_diff = p_diff(X)
plt.plot(X, F1, label="F1")
plt.plot(X, F2, label="F2")
plt.plot(X, F_sum, label="F_sum")
plt.plot(X, F_diff, label="F_diff")

plt.legend()
plt.show()
'''