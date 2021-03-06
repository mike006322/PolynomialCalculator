<h1>Core Polynomial modules</h1>

The Polynomial class stores data as a "term_matrix". This is implemented as a list with
variables given first, then terms.

term_matrix = [['constant', variable1, variable2...], [coefficient, exponent1, exponent2...],...]

For example, 5x^2y + 2x + y + 24 is stored as the following:

[['constant', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]

### Operations:
Polynomial addition, subtraction, multiplication, division, modulo are defined in the Polynomial class.

'gcd' function is also defined.

### Parsing:

The parser takes strings and turns them into term_matrix form.
