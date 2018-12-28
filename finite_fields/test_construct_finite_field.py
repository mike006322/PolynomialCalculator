import unittest
from construct_finite_field import *


class TestParser(unittest.TestCase):

    def test_random_monic(self):
        self.assertEqual(random_monic(2, 2).degree(), 2)

    def test_find_irreducible(self):
        self.assertEqual(type(find_irreducible(2, 8, 3)), Polynomial)
        # print(find_irreducible(2, 8, 3))
        # print(find_irreducible(2, 2, 4))

    def test_find_primitive_element(self):
        print(find_irreducible(2, 2, 3))
        print(find_primitive_element(find_irreducible(2, 2, 4), 2, 4))


if __name__ == '__main__':
    unittest.main()


# x^3 + x^2 + 1.0
# h =  x^4 + x^3 + x^2 + x + 1.0
# order =  5
# f =  x^4 + x + 1.0
# order =  3
# f =  x^4 + x + 1.0
# order =  3
# f =  x^4 + x
# order =  3
# f =  x^4
# order =  5
# f =  x^4 + 1.0
# order =  15
# x^4 + 1.0
