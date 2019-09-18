import unittest
from matrix.matrix_operations import *


class TestMatrixInverse(unittest.TestCase):

    def test_matrix_inverse(self):
        m = get_matrix_inverse([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertEqual(get_matrix_inverse([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), m)
        m = [[0.2, 0.2, 0.0], [-0.2, 0.3, 1.0], [0.2, -0.3, 0.0]]
        self.assertEqual(get_matrix_inverse([[3, 0, 2], [2, 0, -2], [0, 1, 1]]), m)

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
