# Test for construct_finite_field.py
# Place your tests for ZechLogarithmTable, random_monic, find_irreducible, find_primitive_element here.
import unittest
from algebra.construct_finite_field import ZechLogarithmTable, random_monic, find_irreducible, find_primitive_element

class TestConstructFiniteField(unittest.TestCase):
    def test_random_monic(self):
        poly = random_monic(3, 4)
        self.assertEqual(poly.degree(), 4)
        # Check monic: leading coefficient is 1
        self.assertEqual(poly.LT().term_matrix[1][0], 1)

    def test_find_irreducible(self):
        poly = find_irreducible(3, 3)
        self.assertEqual(poly.degree(), 3)
        # Should be monic
        self.assertEqual(poly.LT().term_matrix[1][0], 1)

    def test_zech_logarithm_table(self):
        table = ZechLogarithmTable(2, 3)
        self.assertEqual(table.h.degree(), 3)
        self.assertTrue(hasattr(table, 'poly_to_power'))
        self.assertTrue(hasattr(table, 'power_to_poly'))

if __name__ == '__main__':
    unittest.main()
