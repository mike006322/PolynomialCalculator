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
        self.assertEqual(I.groebner_basis(), [Polynomial('x^2 + -1.0y'), Polynomial('y^2 + -1.0')])
        f = Polynomial('xy^2 - x')
        g = Polynomial('x^2 - y')
        I = Ideal(f, g)
        self.assertEqual(I.groebner_basis(), [Polynomial('y^3 + -1.0y'), Polynomial('xy^2 + -1.0x'), Polynomial('x^2 + -1.0y')])

    def test_reduce(self):
        f = Polynomial('x^3y^2 -x^2y^3 + x')
        g = Polynomial('3x^4y + y^2')
        h = Polynomial('x^5y + y^2')
        G = [f, g, h]
        res = [Polynomial([['constant', 'x', 'y'], [-0.3333333333333333, 1, 2], [1.0, 0, 2]]), Polynomial([['constant', 'x', 'y'], [3.0, 4, 1], [1.0, 0, 2]]), Polynomial([['constant', 'x', 'y'], [1.0, 3, 2], [-1.0, 2, 3], [1.0, 1, 0]])]
        self.assertEqual(Ideal.reduce(G), res)

    def test___eq__(self):
        f = Polynomial('x^2y - 1')
        g = Polynomial('xy^2 - x')
        I = Ideal(f, g)
        s = Polynomial('-x^2 + 1.0y')
        t = Polynomial('-y^2 + 1.0')
        J = Ideal(s, t)
        # print(*I.groebner_basis()) x^2 - 1.0y y^2 - 1.0
        # print(*J.groebner_basis()) -1.0y^2 + 1.0 -1.0x^2 + y
        self.assertFalse(I.groebner_basis() == J.groebner_basis())
        self.assertTrue(I == I)
        self.assertTrue(I == J)


if __name__ == '__main__':
    unittest.main()
