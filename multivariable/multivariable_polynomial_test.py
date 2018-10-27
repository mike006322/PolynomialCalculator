import unittest
import multivariable_polynomial
from multivariable_polynomial import Polynomial

class TestParser(unittest.TestCase):

    def test__init__(self):
        self.assertEqual(Polynomial(0).termMatrix, [[' ']])
        t = [[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
        T = Polynomial(t, char=2)
        self.assertEqual(T.termMatrix, [[' ', 'y', 'x'], [1.0, 1, 2], [1.0, 1, 0]])

    def test_clean(self):
        self.assertEqual(multivariable_polynomial.Polynomial.clean([[' ', 'x', 'y'], [3.0, 2, 0], [1.0, 1, 0], [5.0, 0, 0]]), [[' ', 'x'], [3.0, 2], [1.0, 1], [5.0, 0]])

    def test_equals(self):
        a = Polynomial(0)
        b = Polynomial(0)
        c = 0
        self.assertEqual(a, c)
        self.assertEqual(a, b)
        self.assertFalse(a != b)

    def test_addition(self):
        a = Polynomial('x')
        b = Polynomial(0)
        self.assertTrue(a + b == a)
        a = Polynomial('x', char=2)
        self.assertTrue(a + a == 0)

    def test_subtraction(self):
        a = Polynomial('x + 1')
        b = Polynomial(1)
        c = Polynomial('x')
        self.assertTrue(a - b == c)
        a = Polynomial('x', char=2)
        self.assertTrue(a - a == 0)
        a = Polynomial('3x + 1', char=2)
        b = Polynomial('x + 1', char=2)
        self.assertTrue(a - b == 0)

    def test_multiplication(self):
        a = Polynomial('x')
        b = Polynomial(2)
        c = Polynomial('2x')
        self.assertTrue(a * b == c)
        a = Polynomial('x', char=2)
        b = Polynomial(2, char=2)
        self.assertTrue(a * b == 0)

    def test_division(self):
        # s = 'x^2y + xy^2 + y^2'
        t = 'xy - 1'
        e = 'y^2 - 1'
        # S = Polynomial(s)
        T = Polynomial(t)
        E = Polynomial(e)
        a = Polynomial('x^2 - 1')
        b = Polynomial('x + 1')
        c = Polynomial('x - 1')
        self.assertTrue(a / b == c)
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertTrue(b / b == 1)
        self.assertRaises(multivariable_polynomial.NonFactor, lambda: T / E)
        a = Polynomial('2x^2 - 2', char=2)
        b = Polynomial('x + 1', char=2)
        self.assertTrue(a / b == 0)


    def test_LT(self):
        t = 'xy - 1'
        T = Polynomial(t)
        s = 'x^2y + xy^2 + y^2'
        S = Polynomial(s)
        self.assertEqual(T.LT(), Polynomial('xy'))
        self.assertEqual(S.LT(), Polynomial('x^2y'))

    def test_divides(self):
        t = 'xy - 1'
        T = Polynomial(t)
        s = 'x^2y + xy^2 + y^2'
        S = Polynomial(s)
        self.assertEqual(Polynomial.divides(T, S), True)
        self.assertEqual(Polynomial.divides(S, T), False)

    def test__iter__(self):
        s = 'x^2y + xy^2 + y^2'
        S = multivariable_polynomial.Polynomial(s)
        self.assertEqual([term for term in S], [Polynomial('x^2y'), Polynomial('xy^2'), Polynomial('y^2')])

    def test_mod_poly(self):
        t = [[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
        T = Polynomial(t, char=2)
        self.assertEqual(T.termMatrix, [[' ', 'y', 'x'], [1.0, 1, 2], [1.0, 1, 0]])

    def test_combine_variables(self):
        t = 'x'
        T = multivariable_polynomial.Polynomial(t)
        s = 'x^2y + xy^2 + y^2'
        S = multivariable_polynomial.Polynomial(s)
        res = (Polynomial([[' ', 'x', 'y'], [1.0, 2, 1], [1.0, 1, 2], [1.0, 0, 2]]), Polynomial([[' ', 'x', 'y'], [1.0, 1, 0]]))
        self.assertEqual(Polynomial.combine_variables(S, T), res)
        self.assertEqual(S.termMatrix, [[' ', 'x', 'y'], [1.0, 2, 1], [1.0, 1, 2], [1.0, 0, 2]])
        self.assertEqual(T.termMatrix, [[' ', 'x'], [1.0, 1]])



if __name__ == '__main__':
    unittest.main()
