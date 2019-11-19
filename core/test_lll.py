import unittest
from core.lll import *


class TestLLL(unittest.TestCase):

    def test_lll(self):
        m = lll_reduction([[1, 1, 1], [-1, 0, 2], [3, 5, 6]], 0.75)
        res = [[0, 1, 0], [1, 0, 1], [-1, 0, 2]]
        self.assertEqual(m, res)
        m = [[105, 821, 404, 328], [881, 667, 644, 927], [181, 483, 87, 500], [893, 834, 732, 441]]
        m = [list(map(Rational, x)) for x in m]
        m = lll_reduction(m, 0.75)
        res = [[76, -338, -317, 172], [88, -171, -229, -314], [269, 312, -142, 186], [519, -299, 470, -73]]
        self.assertEqual(m, res)


if __name__ == '__main__':
    unittest.main()
