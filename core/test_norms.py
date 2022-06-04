import unittest
from core.norms import *
from number_objects.primitives.matrix import Matrix


class TestNorms(unittest.TestCase):

    def test_euclidean_norm(self):
        self.assertEqual(euclidean_norm([3, 4]), 5)

    def test_weighted_frobenius_norm(self):
        m = Matrix.identity(2)
        self.assertEqual(weighted_frobenius_norm(m), 2 ** .5)
        m = Matrix([[-1, 1], [0, 2]])
        self.assertEqual(weighted_frobenius_norm(m), 6 ** .5)

    def test_sum_of_squared_corfficients(self):
        m = Matrix.identity(2)
        self.assertEqual(sum_of_squared_coefficietns(m), 2)
        m = Matrix([[-1, 1], [0, 2]])
        self.assertEqual(sum_of_squared_coefficietns(m), 6)


if __name__ == '__main__':
    unittest.main()
