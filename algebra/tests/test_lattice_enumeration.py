import os
import unittest

import numpy as np

from algebra.lattice_enumeration import find_vectors_less_than

_DEBUG = os.environ.get("POLYCALC_TEST_DEBUG") in {"1", "true", "True"}


def _dprint(*args, **kwargs):
    if _DEBUG:
        print(*args, **kwargs)


class TestLattice_enumeation(unittest.TestCase):

    def test_find_vectors_less_than(self):
        t = [[0, 1, 0], [1, 0, 1], [-1, 0, 2]]
        t = np.array(t).transpose()
        short_vectors = find_vectors_less_than(t, 1.1)
        _dprint(short_vectors)
        for i in range(len(short_vectors)):
            _dprint(short_vectors[i])


if __name__ == "__main__":
    unittest.main()
