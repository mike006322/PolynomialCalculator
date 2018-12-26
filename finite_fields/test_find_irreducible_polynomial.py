import unittest
from finite_fields.find_irreducible_polynomial import *


class TestParser(unittest.TestCase):

    def test_random_monic(self):
        self.assertEqual(random_monic(2, 2).degree(), 2)

    def test_find_irreducible(self):
        self.assertEqual(type(find_irreducible(2, 8, 3)), Polynomial)
        print(find_irreducible(2, 8, 3))


if __name__ == '__main__':
    unittest.main()
