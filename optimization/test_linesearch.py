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


if __name__ == '__main__':
    unittest.main()
