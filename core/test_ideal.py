import unittest
from ideal import *
from polynomial import Polynomial


class TestIdeal(unittest.TestCase):

    def test___init__(self):
        f = Polynomial('x^4y')
        g = Polynomial('x^3y^2')
        I = Ideal(f, g)
        self.assertEqual(I.polynomials, (f, g))

    def test___str__(self):
        f = Polynomial('x^4y')
        g = Polynomial('x^3y^2')
        I = Ideal(f, g)
        self.assertEqual(str(I), '<x^4y, x^3y^2>')

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

    def test_solvability_criteria(self):
        f1 = Polynomial('x')
        f2 = Polynomial('y')
        self.assertTrue(Ideal.solvability_criteria((f1, f2), {'x', 'y'}))
        f1 = Polynomial('xy')
        f2 = Polynomial('y')
        self.assertFalse(Ideal.solvability_criteria((f1, f2), {'x', 'y'}))

    def test_solve_system(self):
        f1 = Polynomial('x^2')
        f2 = Polynomial('y')
        f3 = Polynomial('z')
        I = Ideal(f1, f2, f3)
        self.assertEqual(I.solve_system(), '1 solutions: \n[x = 0.0, y = 0, z = 0]')
        f1 = Polynomial('x+2')
        f2 = Polynomial('y')
        f3 = Polynomial('z')
        I = Ideal(f1, f2, f3)
        # print(I.solve_system())
        f1 = Polynomial('x+2')
        f2 = Polynomial('xy+3')
        f3 = Polynomial('z')
        I = Ideal(f1, f2, f3)
        # print(I.solve_system())
        f1 = Polynomial('x')
        f2 = Polynomial('xy')
        f3 = Polynomial('z')
        I = Ideal(f1, f2, f3)
        # print(I.solve_system())
        f1 = Polynomial('x-1')
        f2 = Polynomial('y-2')
        f3 = Polynomial('z-3')
        I = Ideal(f1*f2*f3, f1, f3, f2, f1*f2*f3*Polynomial('xyz+y^12+z^13+8'), f1*f2*f3*Polynomial('z^12+y^40'))
        # print(f1*f2*f3)
        # print(I.solve_system())
        f1 = Polynomial('x1-1')
        f2 = Polynomial('x2-2')
        f3 = Polynomial('x3-3')
        I = Ideal(f1*f2*f3, f1, f3, f2, f1*f2*f3*Polynomial('x1+8'), f1*f2*f3*Polynomial('x3+10'))
        self.assertEqual(I.solve_system(), '1 solutions: \n[x1 = 1.0, x2 = 2.0, x3 = 3.0]')
        f1 = Polynomial('x1-1')
        f2 = Polynomial('x1-17')
        f3 = Polynomial('x1-13')
        f4 = Polynomial('x1-100')
        f = f1*f2*f3*f4
        g1 = Polynomial('x2-1')
        g2 = Polynomial('x3-1')
        g3 = Polynomial('x4-1')
        g4 = Polynomial('x5-1')
        g5 = Polynomial('x6-1')
        g6 = Polynomial('x7-1')
        g7 = Polynomial('x8-1')
        g8 = Polynomial('x9-1')
        g9 = Polynomial('x10-1')
        g10 = Polynomial('x11-1')
        g11 = Polynomial('x12-1')
        g12 = Polynomial('x13-1')
        g13 = Polynomial('x14-1')
        g14 = Polynomial('x15-1')
        g15 = Polynomial('x16-1')
        I = Ideal(f, g1, g2, g3, g4, g5, g6)
        # at Ideal(f, g1, g2, g3, g4, g5, g6), the algorithm begins to take a long time
        # a way to speed it up might be to build in the consideration that adding Polynomial('xn-1') still is a GB
        # then we wouldn't need to calculate GB again.
        # print(I.solve_system())

        f1 = Polynomial('x^3 - 1 -z')
        f2 = Polynomial('y^3 - 2')
        f3 = Polynomial('z^3 + 8')

        I = Ideal(f1, f2, f3, f1*f2*f3*Polynomial('xyz+y^12+z^13+8'), f1*f2*f3*Polynomial('z^12+y^40'))
        # print(f3.solve())
        # print(f1*f2*f3)
        # print(I.solve_system())


if __name__ == '__main__':
    unittest.main()
