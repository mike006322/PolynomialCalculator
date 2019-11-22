import unittest
from core.norms import *
from core.matrix import Matrix


class TestLattice(unittest.TestCase):

    def test_euclidean_norm(self):
        self.assertEqual(euclidean_norm([3, 4]), 5)

    def test_weighted_frobenius_norm(self):
        m = Matrix.identity(2)
        self.assertEqual(weighted_frobenius_norm(m), 2 ** .5)
        m = Matrix([[-1, 1], [0, 2]])
        self.assertEqual(weighted_frobenius_norm(m), 6 ** .5)


if __name__ == '__main__':
    unittest.main()
