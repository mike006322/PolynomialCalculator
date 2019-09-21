import unittest
from numbers import *


class TestInteger(unittest.TestCase):

    def test__init__(self):
        a = Integer(4)
        self.assertEqual(a.value, 4)
        with self.assertRaises(ValueError):
            Integer('s')

    def test__eq__(self):
        self.assertEqual(Integer(2), Integer(2))
        self.assertEqual(Integer(2), 2)
        self.assertEqual(2, Integer(2))
        self.assertTrue(Integer(3) != Integer(2))
        self.assertFalse(Integer(2) != Integer(2))
        self.assertFalse(Integer(3) == Integer(2))

    def test_comparisons(self):
        self.assertTrue(Integer(2) < Integer(3))
        self.assertTrue(Integer(2) <= Integer(3))
        self.assertTrue(Integer(3) > Integer(2))
        self.assertTrue(Integer(3) >= Integer(2))

    def test__int__(self):
        self.assertEqual(int(Integer(2)), 2)

    def test__float__(self):
        self.assertEqual(float(Integer(2)), 2)

    def test__str__(self):
        a = Integer(4)
        self.assertEqual(str(a), '4')

    def test__add__(self):
        a = Integer(2)
        b = Integer(3)
        self.assertEqual(a+b, Integer(5))

    def test__sub__(self):
        a = Integer(2)
        b = Integer(3)
        self.assertEqual(a-b, Integer(-1))

    def test__mul__(self):
        a = Integer(2)
        b = Integer(3)
        self.assertEqual(a*b, Integer(6))
        self.assertEqual(a*8, 16)

    def test__pow__(self):
        a = Integer(2)
        b = Integer(3)
        self.assertEqual(a**b, Integer(8))
        self.assertEqual(2**b, Integer(8))

    def test__mod__(self):
        a = Integer(2)
        b = Integer(3)
        self.assertEqual(a % b, Integer(2))
        self.assertEqual(b % a, Integer(1))

    def test__floordiv__(self):
        self.assertEqual(Integer(3) // Integer(2), 1)

    def test__truediv__(self):
        self.assertEqual(Integer(4)/Integer(2), Integer(2))
        self.assertEqual(Integer(2)/Integer(4), Rational(1, 2))


class TestRational(unittest.TestCase):

    def test__init__(self):
        q = Rational(1, 4)
        self.assertEqual(q.numerator, 1)
        self.assertEqual(q.denominator, 4)
        self.assertEqual(Rational(2), Rational(2, 1))
        self.assertEqual(Rational('1/4'), Rational(1, 4))

    def test__str__(self):
        q = Rational(1, 4)
        self.assertEqual(str(q), '1/4')

    def test_gcd_(self):
        self.assertEqual(Rational.gcd(2, 4), 2)

    def test_normalize(self):
        q = Rational(1, 4)
        p = Rational(2, 8)
        Rational.normalize(p)
        self.assertEqual(p, q)
        q = Rational(-1, 4)
        p = Rational(2, -8)
        Rational.normalize(p)
        self.assertEqual(p, q)
        self.assertEqual(Rational(1, 4), Rational(2, 8))

    def test__float__(self):
        self.assertEqual(float(Rational(2, 4)), .5)

    def test__mul__(self):
        q = Rational(1, 4)
        p = Rational(3, 5)
        self.assertEqual(p*q, Rational(3, 20))
        self.assertEqual(p*2, Rational(6, 5))

    def test__truediv__(self):
        q = Rational(1, 4)
        p = Rational(3, 5)
        self.assertEqual(p/q, Rational(12, 5))

    def test__add__(self):
        self.assertEqual(Rational(1, 2) + Rational(3, 4), Rational(5, 4))
        self.assertEqual(Rational(1, 2) + 1, Rational(3, 2))

    def test__sub__(self):
        self.assertEqual(Rational(1, 2) - Rational(3, 4), Rational(-1, 4))
        self.assertEqual(Rational(1, 2) - 1, Rational(-1, 2))

    def test__pow__(self):
        self.assertEqual(Rational(3, 2)**2, Rational(9, 4))


class TestMakeNumber(unittest.TestCase):

    def test_make_number(self):
        self.assertEqual(make_number('2'), Integer(2))
        self.assertEqual(make_number('2.5'), Rational(5, 2))
        self.assertEqual(make_number('1.5'), Rational(3, 2))


if __name__ == '__main__':
    unittest.main()
