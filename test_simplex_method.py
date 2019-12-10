import unittest
from simplex_method import *
import numpy as np
from scipy import optimize


class TestSimplexMethod(unittest.TestCase):

    def test_simplex_method(self):
        m = np.array([[-2.0, 1.0, -10.0],
                      [1.0, 1.0, 20.0],
                      [-5.0, -10.0, 0.0]])
        res = {'x0': 10.0, 'x1': 10.0, 'optimum': 150.0}
        self.assertEqual(simplex_method(m, dictionary_output=True), res)
        m = np.array([[-2.0, -5.0, -30.0],
                      [3.0, -5.0, -5.0],
                      [8.0, 3.0, 85.0],
                      [-9.0, 7.0, 42.0],
                      [-2.0, -7.0, 0.0]])
        res = {'x0': 5.650602409638554, 'x1': 13.265060240963855, 'optimum': 104.1566265060241}
        self.assertEqual(simplex_method(m, dictionary_output=True), res)
        # y >= -x + 1
        # y >= x + 1
        m = np.array([[-1, -1, -1], [-1, 1, -1], [1, 0, 0]])
        res = 1
        self.assertEqual(simplex_method(m, unrestricted=True, dictionary_output=True)['optimum'], res)
        # y >= -x + 2
        # y >= x - 6
        m = np.array([[-1, -1, -2], [-1, 1, 6], [1, 0, 0]])
        res = -2
        self.assertEqual(simplex_method(m, unrestricted=True, dictionary_output=True)['optimum'], res)
        # y >= -x + 6
        # y >= x - 2
        m = np.array([[-1, -1, -6], [-1, 1, 2], [1, 0, 0]])
        res = 2
        A = np.array([[-1, -1], [-1, 1]])
        b = np.array([-6, 2])
        c = [1, 0]
        print(optimize.linprog(c, A_ub=A, b_ub=b).get('x'))
        print(simplex_method_scipy(m, unrestricted=True))
        self.assertEqual(simplex_method(m, unrestricted=True, dictionary_output=True)['optimum'], res)
        A = np.array([[-1, -1], [-1, 1]])
        b = np.array([-2, 6])
        c = [1, 0]
        # print(optimize.linprog(c, A_ub=A, b_ub=b).get('x'))
        m = np.array([[-1, -1, -1], [-1, 1, -1], [1, 0, 0]])
        print(simplex_method_scipy(m, unrestricted=True))

    def test_get_column(self):
        m = np.array([[-2.0, 1.0, -10.0],
                      [1.0, 1.0, 20.0],
                      [-5.0, -10.0, 0.0]])
        res = np.array([-10, 20, 0])
        self.assertTrue(np.array_equal(get_column(m, -1), res))

    def test_make_unrestricted_variables(self):
        m = np.array([[-2.0, 1.0, -10.0],
                      [1.0, 1.0, 20.0],
                      [-5.0, -10.0, 0.0]])
        res = [[-2.0, 2.0, 1.0, -1.0, -10.0],
               [1.0, -1.0, 1.0, -1.0, 20.0],
               [-1.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, -1.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, -1.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, -1.0, 0.0],
               [-5.0, 5.0, -10.0, 10.0, 0.0]]
        self.assertEqual(make_unrestricted_variables(m).tolist(), res)

    def test_reduce_variables(self):
        m = [10, 20, 10, 30, 150]
        res = [-10, -20, 150]
        self.assertEqual(reduce_variables(m, 4), res)

    def test_restricted_variables(self):
        m = np.array([[-2.0, 1.0, -10.0],
                      [1.0, 1.0, 20.0],
                      [-5.0, -10.0, 0.0]])
        self.assertTrue(np.array_equal(simplex_method(m, unrestricted=True), simplex_method(m, unrestricted=False)))
        m = np.array([[-2.0, -5.0, -30.0],
                      [3.0, -5.0, -5.0],
                      [8.0, 3.0, 85.0],
                      [-9.0, 7.0, 42.0],
                      [-2.0, -7.0, 0.0]])
        self.assertTrue(np.array_equal(simplex_method(m, unrestricted=True), simplex_method(m, unrestricted=False)))


if __name__ == '__main__':
    unittest.main()
