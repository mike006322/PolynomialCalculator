import unittest
from conjugate_gradient import *


class TestLineSearch(unittest.TestCase):

    def test_matrix_euclidean_norm(self):
        m = [[3], [4]]
        self.assertEqual(matrix_euclidean_norm(m), 5)


if __name__ == '__main__':
    unittest.main()
