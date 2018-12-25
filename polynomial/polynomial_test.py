import unittest
import polynomial
from polynomial import Polynomial


class TestParser(unittest.TestCase):

    def test__init__(self):
        self.assertEqual(Polynomial(0).term_matrix, [[' ']])
        t = [[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
        t = Polynomial(t, char=2)
        self.assertEqual(t.term_matrix, [[' ', 'y', 'x'], [1.0, 1, 2], [1.0, 1, 0]])

    def test_clean(self):
        self.assertEqual(Polynomial.clean([[' ', 'x', 'y'], [3.0, 2, 0], [1.0, 1, 0], [5.0, 0, 0]]), [[' ', 'x'], [3.0, 2], [1.0, 1], [5.0, 0]])

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
        self.assertTrue(a + 0 == a)
        self.assertTrue('x' + a == Polynomial('2x'))
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
        self.assertTrue('x' * b == c)
        self.assertTrue(a * 2 == c)
        a = Polynomial('x', char=2)
        b = Polynomial(2, char=2)
        self.assertTrue(a * b == 0)

    def test_pow(self):
        x = Polynomial('x')
        print(x**2)

    def test_division(self):
        t = Polynomial('xy - 1')
        s = Polynomial('y^2 - 1')
        a = Polynomial('x^2 - 1')
        b = Polynomial('x + 1')
        c = Polynomial('x - 1')
        self.assertTrue(a / b == c)
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertTrue(b / b == 1)
        self.assertRaises(polynomial.NonFactor, lambda: t / s)
        a = Polynomial('2x^2 - 2', char=2)
        b = Polynomial('x + 1', char=2)
        self.assertTrue(a / b == 0)

    def test_LT(self):
        t = Polynomial('xy - 1')
        s = Polynomial('x^2y + xy^2 + y^2')
        self.assertEqual(t.LT(), Polynomial('xy'))
        self.assertEqual(s.LT(), Polynomial('x^2y'))

    def test__iter__(self):
        S = Polynomial('x^2y + xy^2 + y^2')
        self.assertEqual([term for term in S], [Polynomial('x^2y'), Polynomial('xy^2'), Polynomial('y^2')])

    def test_mod_char(self):
        t = [[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
        t = Polynomial(t, char=2)
        self.assertEqual(t.term_matrix, [[' ', 'y', 'x'], [1.0, 1, 2], [1.0, 1, 0]])

    def test_combine_variables(self):
        t = Polynomial('x')
        s = Polynomial('x^2y + xy^2 + y^2')
        res = (Polynomial([[' ', 'x', 'y'], [1.0, 2, 1], [1.0, 1, 2], [1.0, 0, 2]]), Polynomial([[' ', 'x', 'y'], [1.0, 1, 0]]))
        self.assertEqual(Polynomial.combine_variables(s, t), res)
        self.assertEqual(s.term_matrix, [[' ', 'x', 'y'], [1.0, 2, 1], [1.0, 1, 2], [1.0, 0, 2]])
        self.assertEqual(t.term_matrix, [[' ', 'x'], [1.0, 1]])

    def test_mod(self):
        self.assertEqual(Polynomial('x^2y + xy^2 + y^2') % Polynomial('x'), Polynomial('y^2'))
        self.assertEqual(Polynomial('x^2y + xy^2 + y^2') % 'x', Polynomial('y^2'))
        # self.assertEqual('x^2y + xy^2 + y^2' % Polynomial('x'), Polynomial('y^2'))
        # __rmod__ cannot override the string's LHS __mod__ operator, see bug at: https://bugs.python.org/issue28598

    def test_degree(self):
        self.assertEqual(Polynomial('x + x^2').degree(), 2)
        self.assertEqual(Polynomial('8 + x + x^2').degree(), 2)
        self.assertEqual(Polynomial('8 + x + y + y^3 + x^2').degree(), 3)
        self.assertEqual(Polynomial('8 + x + y + y^3x^3 + x^2').degree(), 6)


if __name__ == '__main__':
    unittest.main()
