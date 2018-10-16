<h1>Multivariable Polynomials</h1>

Manipulation of polynomials is done by converting them to a standard form, the "termMatrix". This form is implemented as a list where the first element is a list of variables. The following lists are terms in the polynomial.

termMatrix = [[' ', variable1, variable2...], [coefficient, exponent1, exponent2...],...]

For example, 5x^2y+2x+y+24 is represented as the following:

[[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]



### Similar projects:
- Sympy
    https://github.com/sympy/sympy

- http://cocoa.dima.unige.it/ written in C++ and CoCa language

- jasymchat - Computer Algebra System written in Java, won't run on phone, seems defunct

Other projects don't emphasize the GUI.
Instead they offer lists of useful commands as options for the user to run.

Near-term goal: create a program that turns strings that represent polynomials into coded polynomials
As it converts to coded language it prints "Input: ", Polynomal(input) to confirm understanding

web GUI?
