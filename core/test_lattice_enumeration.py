import unittest
from core.lattice_enumeration import *


class TestLattice_enumeation(unittest.TestCase):

    def test_find_vectors_less_than(self):
        t = [[0, 1, 0],
             [1, 0, 1],
             [-1, 0, 2]]
        t = np.array(t).transpose()
        short_vectors = find_vectors_less_than(t, 1.1)
        print(short_vectors)
        for i in range(len(short_vectors)):
            print(short_vectors[i])


if __name__ == '__main__':
    unittest.main()
