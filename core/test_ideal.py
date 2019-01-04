import unittest
from core.ideal import *
from core.polynomial import Polynomial


class TestIdeal(unittest.TestCase):

    def test___init__(self):
        f = Polynomial('x^4y')
        g = Polynomial('x^3y^2')
        I = Ideal(f, g)
        self.assertEqual(I.polynomials, (f, g))

    # def test_s_polynomial(self):
    #     f = Polynomial('x^4y')
    #     g = Polynomial('x^3y^2')
    #     self.assertEqual(Ideal.s_polynomial(f, g), Polynomial('−x^3y^3 + x^2 − (1/3)y^3'))


if __name__ == '__main__':
    unittest.main()
