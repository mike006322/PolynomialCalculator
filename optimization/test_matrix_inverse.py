import unittest
from matrix_inverse import *


class TestMatrixInverse(unittest.TestCase):

    def test_matrix_inverse(self):
        m = get_matrix_inverse([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertEqual(get_matrix_inverse([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), m)
        m = [[0.2, 0.2, 0.0], [-0.2, 0.3, 1.0], [0.2, -0.3, 0.0]]
        self.assertEqual(get_matrix_inverse([[3, 0, 2], [2, 0, -2], [0, 1, 1]]), m)


if __name__ == '__main__':
    unittest.main()
