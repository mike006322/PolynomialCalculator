import unittest
from linesearch import *


class TestLineSearch(unittest.TestCase):

    def test_euclidean_norm(self):
        v = (1, 2)
        u = (0, 1)
        norm = euclidean_norm
        self.assertEqual(norm(v), 5**.5)
        self.assertEqual(euclidean_norm(u), 1)

    def test_steepest_descent(self):
        f = Polynomial('x1^2+2x1x2^2+x2^4')
        x = (1, 1)
        self.assertEqual(steepest_descent(f, x), [-0.4472135954999579, -0.8944271909999159])

    def test_interpolate(self):
        phi = Polynomial('x')
        self.assertEqual(interpolate(phi, 0, 1), 0)
        phi = Polynomial('x^2')
        self.assertEqual(interpolate(phi, 2, 4), 2)
        self.assertEqual(interpolate(phi, -2, 4), 0)

    def test_find_step_length(self):
        f = Polynomial('x1^2+x2^3')
        x = [1, 1]
        print(find_step_length(f, x, [3, 3]))


if __name__ == '__main__':
    unittest.main()
