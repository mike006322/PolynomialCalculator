import unittest
from core.ideal import *
from core.polynomial import Polynomial


class TestIdeal(unittest.TestCase):

    def test___init__(self):
        f = Polynomial('x^4y')
        g = Polynomial('x^3y^2')
        I = Ideal(f, g)
        self.assertEqual(I.polynomials, (f, g))

    def test_s_polynomial(self):
        f = Polynomial('x^3y^2 -x^2y^3 + x')
        g = Polynomial('3x^4y + y^2')
        # print(Polynomial('−x^3y^3 + x^2 − (1/3)y^3').term_matrix)
        # parser doesn't support rational inputs yet
        self.assertEqual(Ideal.s_polynomial(f, g), Polynomial([['constant', 'x', 'y'], [-1.0, 3, 3], [1.0, 2, 0], [-0.3333333333333333, 0, 3]]))

    def test_groebner_basis(self):
        f = Polynomial('x^2y - 1')
        g = Polynomial('xy^2 - x')
        I = Ideal(f, g)
        print(*I.groebner_basis())
        f = Polynomial('xy^2 - x')
        g = Polynomial('x^2 - y')
        I = Ideal(f, g)
        print(*I.groebner_basis())


if __name__ == '__main__':
    unittest.main()
