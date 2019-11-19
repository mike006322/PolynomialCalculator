import unittest
from core.norms import *


class TestLattice(unittest.TestCase):

    def test_euclidean_norm(self):
        self.assertEqual(euclidean_norm([3, 4]), 5)


if __name__ == '__main__':
    unittest.main()
