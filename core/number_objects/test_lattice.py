import unittest
from number_objects.lattice import *


class TestLattice(unittest.TestCase):

    def test_center_density(self):
        R = Lattice([[1, 1, 1], [-1, 0, 2], [3, 5, 6]])
        self.assertEqual(R.center_density, 0.041666666666666664)


if __name__ == '__main__':
    unittest.main()
