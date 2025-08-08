import unittest

from polynomials.primitives.matrix import (
    Matrix,
    Vector,
    column_sub_matrix,
    constant_times_vector,
    get_integer_ref,
    get_matrix_inverse,
    get_nullspace,
    gram_schmidt,
    matrix_times_matrix,
    matrix_times_vector,
    transpose_matrix,
    vector_plus_vector,
    vector_times_matrix,
    vector_times_vector,
)


class TestMatrix(unittest.TestCase):

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
        x = [[12, 7, 3], [4, 5, 6], [7, 8, 9]]
        y = [[5, 8, 1, 2], [6, 7, 3, 0], [4, 5, 9, 1]]
        self.assertEqual(
            matrix_times_matrix(x, y), [[114, 160, 60, 27], [74, 97, 73, 14], [119, 157, 112, 23]]
        )

    def test_column_sub_matrix(self):
        m = [[12, 7, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(column_sub_matrix(m, 2), [[12, 7], [4, 5], [7, 8]])

    def test_get_integer_ref(self):
        m = [[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]]
        # assert get_integer_ref(m) == [[1, -2, 0, -1, 3], [0, 0, 1, 2, -2], [0, 0, 0, 0, 0]]
        res = [
            [1.0, -2.0, 0.0, -1.0, 3.0],
            [-0.0, -0.0, -1.0, -2.0, 2.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
        ]
        self.assertEqual(get_integer_ref(m), res)
        m = transpose_matrix(m)
        int_ref = get_integer_ref(m)
        res = [
            [5.0, -0.0, 1.0],
            [0.0, 5.0, 13.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [-0.0, 0.0, 0.0],
        ]
        self.assertEqual(int_ref, res)

    def test_get_nullspace(self):
        m = [[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]]
        N = get_nullspace(m)
        self.assertEqual(N, [[2, 1, -3], [1, 0, 0], [0, -2, 2], [0, 1, 0], [0, 0, 1]])
        test_vec = transpose_matrix([[1, 2, 3]])
        self.assertEqual(matrix_times_matrix(m, matrix_times_matrix(N, test_vec)), [[0], [0], [0]])
        m = [
            [4, 4, 4, 4, 4, 124, 0, 0, 0, 0, 0, 0, 0],
            [4, 12, 36, 108, 324, 0, 124, 0, 0, 0, 0, 0, 0],
            [4, 36, 324, 2916, 26244, 0, 0, 124, 0, 0, 0, 0, 0],
            [62, 0, 0, 0, 0, 0, 0, 0, 124, 0, 0, 0, 0],
            [0, 62, 0, 0, 0, 0, 0, 0, 0, 124, 0, 0, 0],
            [0, 0, 62, 0, 0, 0, 0, 0, 0, 0, 124, 0, 0],
            [0, 0, 0, 62, 0, 0, 0, 0, 0, 0, 0, 124, 0],
            [31, 31, 31, 31, 31, 0, 0, 0, 0, 0, 0, 0, 124],
        ]
        N = get_nullspace(m)
        res = [
            [-62, 0, 0, 0, 62, 0, -160, -13120, 31, 0, 0, 0, 0],
            [0, -62, 0, 0, 62, 0, -156, -13104, 0, 31, 0, 0, 0],
            [0, 0, -62, 0, 62, 0, -144, -12960, 0, 0, 31, 0, 0],
            [0, 0, 0, -62, 62, 0, -108, -11664, 0, 0, 0, 31, 0],
            [0, 0, 0, 0, -124, 4, 324, 26244, 0, 0, 0, 0, 31],
        ]
        self.assertEqual(transpose_matrix(N), res)

    def test_scalar_multiplication(self):
        M = Matrix([[-3, 6, -1, 1, -7], [1, -2, 2, 3, -1], [2, -4, 5, 8, -4]])
        res = Matrix([[-6, 12, -2, 2, -14], [2, -4, 4, 6, -2], [4, -8, 10, 16, -8]])
        self.assertEqual(M * 2, res)

    def test_multiplication(self):
        m1 = Matrix([[1, 0], [0, 1]])
        m2 = Matrix([[2, 3], [4, 5]])
        self.assertEqual(m1 * m2, m2)

    def test_shape(self):
        m = Matrix([[1, 0], [0, 1]])
        self.assertEqual(m.shape, (2, 2))

    def test___add__(self):
        m = Matrix([[1, 0], [0, 1]])
        res = Matrix([[2, 0], [0, 2]])
        self.assertEqual(m + m, res)

    def test_zeroes(self):
        m = Matrix.zeroes(5)
        res = Matrix([[0, 0, 0, 0, 0]])
        self.assertEqual(m, res)
        m = Matrix.zeroes((3, 3))
        res = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertEqual(m, res)

    def test_identity(self):
        res = Matrix([[1, 0], [0, 1]])
        self.assertEqual(Matrix.identity(2), res)

    def test_gram_schmidt(self):
        m = gram_schmidt([Vector([3, 1]), Vector([2, 2])])
        res = [[3, 1], [-2 / 5, 6 / 5]]
        for i in range(len(m)):
            for j in range(len(m[0])):
                self.assertAlmostEqual(m[i][j], res[i][j])
        m = gram_schmidt([Vector([4, 1, 2]), Vector([4, 7, 2]), Vector([3, 1, 7])])
        res = [[4, 1, 2], [-8 / 7, 40 / 7, -4 / 7], [-11 / 5, 0, 22 / 5]]
        for i in range(len(m)):
            for j in range(len(m[0])):
                self.assertAlmostEqual(m[i][j], res[i][j])

    def test_concatenate(self):
        m = Matrix([[1, 0], [0, 1]])
        m2 = Matrix([[1, 1]])
        m3 = m.concatenate(m2)
        res = Matrix([[1, 0], [0, 1], [1, 1]])
        self.assertEqual(m3, res)
        m3 = m.concatenate(m2.transpose(), axis=1)
        res = Matrix([[1, 0, 1], [0, 1, 1]])
        self.assertEqual(m3, res)
        m3 = m.concatenate([])
        self.assertEqual(m3, m)

    def test_determinant(self):
        m = Matrix.identity(10)
        det = m.determinant()
        res = 1
        self.assertEqual(det, res)
        m = Matrix([[1, 0, 0], [0, 1, 0], [1, 0, 0]])
        det = m.determinant()
        res = 0
        self.assertEqual(det, res)
        m = Matrix([[1, 4, 5], [0, 2, 6], [0, 0, 3]])
        det = m.determinant()
        res = 6
        self.assertEqual(det, res)


if __name__ == "__main__":
    unittest.main()
