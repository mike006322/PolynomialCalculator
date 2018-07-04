import unittest
import multivariable_polynomial

class TestParser(unittest.TestCase):

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
        a = multivariable_polynomial.Polynomial('x^2 - 1')
        b = multivariable_polynomial.Polynomial('x + 1')
        c = multivariable_polynomial.Polynomial('x - 1')
        self.assertTrue(a / b == c)
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertTrue(b / b == 1)


if __name__ == '__main__':
    unittest.main()
