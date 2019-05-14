from ideal import *

# Polynomial multiplication
f1 = Polynomial('3x^2 + 7x+13')
f2 = Polynomial('x^3 + 10x^2 + 169x')
# print(f1*f2)


# Polynomial division
# print(division_string(f1, f2))

h = Polynomial('2x - 2')
g = Polynomial('x^2-1')
# print(division_string(g, h))

# Rational coefficient outputs
f = Polynomial('x^2y^3 + x^2 + 4y + 13')
# print(3*f/4)


# Polynomials over GF(2)
f = Polynomial('7x^4 + 8x^3 + 9x^2 + 10x + 1', 2)
# the second input to "Polynomial" is an optional input for field characteristic. Default is 0.
# print(f)



# Solve single variable polynomials
f = Polynomial('x^3 + 10x^2 + 169x')
# print(f.solve())



# Polynomial GCD
g = Polynomial('x^5 + x^14 + 13')
f1 = g*Polynomial('x^2 - 1')
f2 = g*Polynomial('x')
# print(gcd(f1, f2))


# find Groebner Basis for f1, f2, f3
# note rational coefficient outputs
f1 = Polynomial('xy + x + y+4')
f2 = Polynomial('x^2 + 8xy + 16')
I = Ideal(f1, f2)
# print(*I.groebner_basis())


# check that g1, g2, g3 is a Groebner Basis
g1 = Polynomial('x^3 + 2y + z')
g2 = Polynomial('3y^4 + 7y + 3z')
g3 = Polynomial('z^2 + 6z + 2')
I = Ideal(g1, g2, g3)
# print(*I.groebner_basis())


# solve system of multivariable polynomials
f1 = Polynomial('x1 - 1')
f2 = Polynomial('x2 - 2')
f3 = Polynomial('x3 - 3')
I = Ideal(f1, f3, f2, f1*f2*f3*Polynomial('x1+8'), f1*f2*f3*Polynomial('x3+10'))
# print(f1*f2*f3)
# print(I.solve_system())

f1 = Polynomial('x^2 - 1 - z')
f2 = Polynomial('y^2 - 2')
f3 = Polynomial('z^5 + 8')

I = Ideal(f1, f2, f3, f1*f2*f3*Polynomial('xyz+y^12+z^13+8'), f1*f2*f3*Polynomial('z^12+y^40'))
print(I.solve_system())


