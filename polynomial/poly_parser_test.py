import unittest
from poly_parser import *
from orderings import order_lex


class TestParser(unittest.TestCase):

    def test_find_vars(self):
        """
        Input is a list of terms after replace(" ", "").replace("-","+-").replace("*", "").lower().split("+"),
        Output is a set of discovered variables
        """
        self.assertEqual(find_vars(['x', 'y', 'z']), {'x', 'y', 'z'})
        self.assertEqual(find_vars(['x1^2x2^3', '-9z^4t^2', '7x^2x2^6']), {'x2', 'z', 't', 'x', 'x1'})

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_parse_poly(self):
        # poly = 'z^3*4x^2+8+y*z^4'
        # poly = '2*X^2y-x-2'
        test1 = 'x1^2*x2^3 - 9Z^4T^2 + 7x1^2x2^6'
        self.assertEqual(order_lex(parse_poly(test1)), [[' ', 't', 'x1', 'x2', 'z'], [-9.0, 2, 0, 0, 4], [7.0, 0, 2, 6, 0], [1.0, 0, 2, 3, 0]])
        self.assertEqual(parse_poly('x+1'), [[' ', 'x'], [1.0, 1], [1.0, 0]])
        self.assertEqual(parse_poly('x^2 + -1.0'), [[' ', 'x'], [1.0, 2], [-1.0, 0]])


if __name__ == '__main__':
    unittest.main()
