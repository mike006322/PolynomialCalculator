<h1>Multivariable Polynomials</h1>

Manipulation of polynomials is done by converting them to a standard form, the "termMatrix". This form is implemented as a list where the first element is a list of variables after a blank string. The following lists are terms in the polynomial.

termMatrix = [[' ', variable1, variable2...], [coefficient, exponent1, exponent2...],...]

For example, 5x^2y+2x+y+24 is represented as the following:

[[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
