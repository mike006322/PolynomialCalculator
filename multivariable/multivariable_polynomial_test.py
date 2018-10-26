import unittest
import multivariable_polynomial
from multivariable_polynomial import Polynomial

class TestParser(unittest.TestCase):

    def test_clean(self):
        self.assertEqual(multivariable_polynomial.Polynomial.clean([[' ', 'x', 'y'], [3.0, 2, 0], [1.0, 1, 0], [5.0, 0, 0]]), [[' ', 'x'], [3.0, 2], [1.0, 1], [5.0, 0]])

    def test_equals(self):
        a = multivariable_polynomial.Polynomial(0)
        b = multivariable_polynomial.Polynomial(0)
        c = 0
        self.assertEqual(a, c)
        self.assertEqual(a, b)
        self.assertFalse(a != b)

    def test_addition(self):
        a = multivariable_polynomial.Polynomial('x')
        b = multivariable_polynomial.Polynomial(0)
        self.assertTrue(a + b == a)

    def test_subtraction(self):
        a = multivariable_polynomial.Polynomial('x + 1')
        b = multivariable_polynomial.Polynomial(1)
        c = multivariable_polynomial.Polynomial('x')
        self.assertTrue(a - b == c)

    def test_multiplication(self):
        a = multivariable_polynomial.Polynomial('x')
        b = multivariable_polynomial.Polynomial(2)
        c = multivariable_polynomial.Polynomial('2x')
        self.assertTrue(a * b == c)

    def test_division(self):
        # s = 'x^2y + xy^2 + y^2'
        t = 'xy - 1'
        e = 'y^2 - 1'
        # S = multivariable_polynomial.Polynomial(s)
        T = multivariable_polynomial.Polynomial(t)
        E = multivariable_polynomial.Polynomial(e)
        a = multivariable_polynomial.Polynomial('x^2 - 1')
        b = multivariable_polynomial.Polynomial('x + 1')
        c = multivariable_polynomial.Polynomial('x - 1')
        self.assertTrue(a / b == c)
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertTrue(b / b == 1)
        self.assertRaises(multivariable_polynomial.NonFactor, lambda: T / E)

    def test_LT(self):
        t = 'xy - 1'
        T = multivariable_polynomial.Polynomial(t)
        s = 'x^2y + xy^2 + y^2'
        S = multivariable_polynomial.Polynomial(s)
        self.assertEqual(T.LT(), Polynomial('xy'))
        self.assertEqual(S.LT(), Polynomial('x^2y'))

    def test_divides(self):
        t = 'xy - 1'
        T = multivariable_polynomial.Polynomial(t)
        s = 'x^2y + xy^2 + y^2'
        S = multivariable_polynomial.Polynomial(s)
        self.assertEqual(Polynomial.divides(T, S), True)
        self.assertEqual(Polynomial.divides(S, T), False)

    def test__iter__(self):
        s = 'x^2y + xy^2 + y^2'
        S = multivariable_polynomial.Polynomial(s)
        self.assertEqual([term for term in S], [Polynomial('x^2y'), Polynomial('xy^2'), Polynomial('y^2')])



if __name__ == '__main__':
    unittest.main()
