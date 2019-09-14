import unittest
from backtracking_linesearch import *


class TestBackTrackingLineSearch(unittest.TestCase):

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

    def test_vector_plus_vector(self):
        v1 = [2, 3]
        v2 = [5, 7]
        self.assertEqual(vector_plus_vector(v1, v2), [7, 10])

    def test_vector_times_vector(self):
        v1 = [2, 3]
        v2 = [5, 7]
        self.assertEqual(vector_times_vector(v1, v2), 31)

    def test_constant_times_vector(self):
        v1 = [2, 3]
        self.assertEqual(constant_times_vector(5, v1), [10, 15])

    def test_matrix_times_vector(self):
        m = [[1, 2], [3, 5]]
        v = [2, 3]
        self.assertEqual(matrix_times_vector(m, v), [8, 21])


if __name__ == '__main__':
    unittest.main()
