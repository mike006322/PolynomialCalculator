import unittest
from core.vector import *
from core.polycalc_numbers import *


class TestVector(unittest.TestCase):

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
        t = Vector(["3/2", "4/5", "1/4"]) * 2
        eight_five = Rational(8, 5)
        half = Rational(1, 2)
        res = [3, eight_five, half]


if __name__ == '__main__':
    unittest.main()
