import unittest
from simplex_method import *


class TestSimplexMethod(unittest.TestCase):

    def test_simplex_method(self):
        m = np.array([[-2.0, 1.0, -10.0], [1.0, 1.0, 20.0], [-5.0, -10.0, 0.0]])
        print(simplex_method(m))
        m = np.array([[-2.0, -5.0, -30.0], [3.0, -5.0, -5.0], [8.0, 3.0, 85.0], [-9.0, 7.0, 42.0], [-2.0, -7.0, 0.0]])
        print(simplex_method(m))


if __name__ == '__main__':
    unittest.main()
