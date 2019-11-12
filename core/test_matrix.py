import unittest
from matrix import *


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

    def test_vector_times_matrix(self):
        m = [[1, 2], [3, 5]]
        v = [2, 3]
        self.assertEqual(vector_times_matrix(v, m), [11, 19])

    # def test_get_nullspace_numpy(self):
    #     m = np.array([[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]])
    #     N = get_nullspace_numpy(m)
    #     self.assertEqual(N.tolist(), np.array([[2, 1, -3], [1, 0, 0], [0, -2, 2], [0, 1, 0], [0, 0, 1]]).tolist())
    #     test_vec = np.array([[1, 2, 3]]).transpose()
    #     self.assertEqual((m @ (N @ test_vec)).tolist(), [[0], [0], [0]])

    # def test_get_left_nullspace_numpy(self):
    #     m = np.array([[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]])
    #     left_nullspace = get_left_nullspace_numpy(m)
    #     self.assertEqual(left_nullspace.tolist(), [[-1, -13, 5]])

    def test_matrix_times_matrix(self):
        x = [[12, 7, 3],
             [4, 5, 6],
             [7, 8, 9]]
        y = [[5, 8, 1, 2],
             [6, 7, 3, 0],
             [4, 5, 9, 1]]
        self.assertEqual(matrix_times_matrix(x, y), [[114, 160, 60, 27], [74, 97, 73, 14], [119, 157, 112, 23]])

    def test_column_sub_matrix(self):
        m = [[12, 7, 3],
             [4, 5, 6],
             [7, 8, 9]]
        self.assertEqual(column_sub_matrix(m, 2), [[12, 7], [4, 5], [7, 8]])


if __name__ == '__main__':
    unittest.main()
