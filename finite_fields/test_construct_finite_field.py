import unittest
from construct_finite_field import *


class TestParser(unittest.TestCase):

    def test_random_monic(self):
        self.assertEqual(random_monic(2, 2).degree(), 2)

    def test_find_irreducible(self):
        self.assertEqual(type(find_irreducible(2, 3)), Polynomial)
        # print(find_irreducible(2, 3))
        # print(find_irreducible(2, 4))

    def test_find_primitive_element(self):
        print(find_irreducible(2, 3))
        self.assertTrue(find_primitive_element(find_irreducible(2, 4), 2, 4) == Polynomial('x') or Polynomial('x^2+1'))
        pass

    def test_Zech__init__(self):
        z = ZechLogarithmTable(2, 2)
        self.assertEqual(z.h, Polynomial('x^2 + x + 1.0', 2))
        self.assertEqual(len(z.power_to_poly), 3)
        z = ZechLogarithmTable(2, 4)
        self.assertEqual(len(z.power_to_poly), 15)


if __name__ == '__main__':
    unittest.main()
