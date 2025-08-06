import unittest
from core.number_objects.polynomial import Polynomial, random_monic, find_irreducible, find_primitive_element, ZechLogarithmTable
from construct_finite_field import random_monic, find_irreducible, find_primitive_element, ZechLogarithmTable


class TestConstructFiniteFields(unittest.TestCase):

    def test_random_monic(self):
        self.assertEqual(random_monic(2, 2).degree(), 2)

    def test_find_irreducible(self):
        self.assertEqual(type(find_irreducible(2, 3)), Polynomial)
        # print(find_irreducible(2, 3))
        # print(find_irreducible(2, 4))

    def test_find_primitive_element(self):
        # print(find_irreducible(2, 3))
        self.assertTrue(find_primitive_element(find_irreducible(2, 4), 2, 4) == Polynomial('x') or Polynomial('x^2+1'))

    def test_ZechLogarithmTable(self):
        z = ZechLogarithmTable(2, 2)
        self.assertEqual(z.h, Polynomial('x^2 + x + 1.0', 2))
        self.assertEqual(len(z.power_to_poly), 3)
        z = ZechLogarithmTable(2, 4, Polynomial('1+x+x^4', 2))
        self.assertEqual(len(z.power_to_poly), 15)
        d = {'1': 0, 'x': 1, 'x^2': 2, 'x^3': 3, 'x + 1.0': 4, 'x^2 + x': 5, 'x^3 + x^2': 6, 'x^3 + x + 1.0': 7, 'x^2 + 1.0': 8, 'x^3 + x': 9, 'x^2 + x + 1.0': 10, 'x^3 + x^2 + x': 11, 'x^3 + x^2 + x + 1.0': 12, 'x^3 + x^2 + 1.0': 13, 'x^3 + 1.0': 14}
        self.assertEqual(z.poly_to_power, d)
        self.assertEqual(z.multiply(Polynomial('x^3+x+1', 2), Polynomial('x^2+x', 2)), Polynomial('x^3 + x^2 + x + 1.0', 2))


if __name__ == '__main__':
    unittest.main()
