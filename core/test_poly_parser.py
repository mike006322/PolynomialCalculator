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
        test2 = '-x^3 + x^2'
        self.assertEqual(order_lex(parse_poly(test1)), [['constant', 't', 'x1', 'x2', 'z'], [-9.0, 2, 0, 0, 4], [7.0, 0, 2, 6, 0], [1.0, 0, 2, 3, 0]])
        self.assertEqual(parse_poly('x+1'), [['constant', 'x'], [1.0, 1], [1.0, 0]])
        self.assertEqual(parse_poly('x^2 + -1.0'), [['constant', 'x'], [1.0, 2], [-1.0, 0]])
        self.assertEqual(parse_poly(test2), [['constant', 'x'], [-1.0, 3], [1.0, 2]])
        test3 = 'x^100'
        self.assertEqual(parse_poly(test3), [['constant', 'x'], [1, 100]])

    def test_find_corresponding_right_parenthesis(self):
        test = "()"
        self.assertEqual(find_corresponding_right_parenthesis(test, 0), 1)
        test = "(abc)"
        self.assertEqual(find_corresponding_right_parenthesis(test, 0), 4)
        test = "((abc))"
        self.assertEqual(find_corresponding_right_parenthesis(test, 0), 6)
        self.assertEqual(find_corresponding_right_parenthesis(test, 1), 5)
        test = "((abc)"
        self.assertRaises(InputError, find_corresponding_right_parenthesis, test, 0)

    def test_parse_function(self):
        f = 'x+2'
        res = [('x', 'variable'), ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = 'x^3+2'
        res = [('x', 'variable'), ('^', 'operation'), ('3', 'number'), ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = 'x**3+2'
        res = [('x', 'variable'), ('**', 'operation'), ('3', 'number'), ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = 'x**(3*15)+2'
        res = [('x', 'variable'), ('**', 'operation'), [('3', 'number'), ('*', 'operation'), ('5', 'number')], ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)

    def test_order_prefix(self):
        f = 'x**2'
        res = [('**', 'operation'), ('x', 'variable'), ('2', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '2x**2'
        res = [('*', 'operation'), ('2', 'number'), ('**', 'operation'), ('x', 'variable'), ('2', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '(4-x)*(5+y)'
        res = [('*', 'operation'), ('-', 'operation'), ('4', 'number'), ('x', 'variable'), ('+', 'operation'), ('5', 'number'), ('y', 'variable')]
        self.assertEqual(order_prefix(parse_function(f)), res)

    def test_construct_expression_tree(self):
        f = '(4-x)*(5+y)'
        t = construct_expression_tree(order_prefix(parse_function(f)))
        self.assertEqual(t.left.value, '-')
        self.assertEqual(t.left.left.value, '4')
        self.assertEqual(t.left.right.value, 'x')
        self.assertEqual(t.right.left.value, '5')
        self.assertEqual(t.right.right.value, 'y')


if __name__ == '__main__':
    unittest.main()
