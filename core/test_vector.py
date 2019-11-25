import unittest
from core.vector import *
from core.matrix import *
from core.polycalc_numbers import Rational


class TestVector(unittest.TestCase):

    def test__init__(self):
        t = Vector([1, 2, 3])
        res = [1, 2, 3]
        self.assertEqual(t, res)
        t = Vector(1, 2, 3)
        res = [1, 2, 3]
        self.assertEqual(t, res)

    def test_vector_dot(self):
        t = Vector([1, 2, 3]).dot(Vector([4, 5, 6]))
        res = Rational(32, 1)
        self.assertEqual(t, res)

    def test_vector_proj_coeff(self):
        t = Vector([1, 1, 1]).proj_coeff(Vector([-1, 0, 2]))
        res = Rational(1, 3)
        self.assertEqual(t, res)

    def test_vector_proj(self):
        t = Vector([Rational(1), Rational(1), Rational(1)]).proj(Vector([Rational(-1), Rational(0), Rational(2)]))
        third = Rational(1, 3)
        res = [third, third, third]
        self.assertEqual(t, res)

    def test_subtraction(self):
        t = Vector([1, 2, 3]) - Vector([6, 5, 4])
        res = [-5, -3, -1]
        self.assertEqual(t, res)

    def test_multiplication(self):
        t = Vector([Rational(3, 2), Rational(4, 5), Rational(1, 4)]) * 2
        eight_five = Rational(8, 5)
        half = Rational(1, 2)
        res = [3, eight_five, half]
        self.assertEqual(t, res)


if __name__ == '__main__':
    unittest.main()
