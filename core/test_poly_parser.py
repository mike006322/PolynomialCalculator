import unittest
from poly_parser import *


class TestParser(unittest.TestCase):

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

    def test_hand_negative_inputs(self):
        f = '-x'
        res = [('0', 'number'), ('-', 'operation'), ('x', 'variable')]
        self.assertEqual(handle_negative_inputs(parse_function(f)), res)
        f = '2-x'
        res = [('2', 'number'), ('-', 'operation'), ('x', 'variable')]
        self.assertEqual(handle_negative_inputs(parse_function(f)), res)
        f = '2^(-x)'
        res = [('2', 'number'), ('**', 'operation'), [('0', 'number'), ('-', 'operation'), ('x', 'variable')]]
        self.assertEqual(handle_negative_inputs(parse_function(f)), res)

    def test_parse_function(self):
        f = 'x+2'
        res = [('x', 'variable'), ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = 'x^3+2'
        res = [('x', 'variable'), ('**', 'operation'), ('3', 'number'), ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = 'x**3+2'
        res = [('x', 'variable'), ('**', 'operation'), ('3', 'number'), ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = 'x**(3*15)+2'
        res = [('x', 'variable'), ('**', 'operation'), [('3', 'number'), ('*', 'operation'), ('5', 'number')], ('+', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = '3*(2x)'
        res = [('3', 'number'), ('*', 'operation'), [('2', 'number'), ('x', 'variable')]]
        self.assertEqual(parse_function(f), res)
        f = '2xy + y^3'
        res = [('2', 'number'), ('x', 'variable'), ('y', 'variable'), ('+', 'operation'), ('y', 'variable'), ('**', 'operation'), ('3', 'number')]
        self.assertEqual(parse_function(f), res)
        f = '8 + x + x^2'
        res = [('8', 'number'), ('+', 'operation'), ('x', 'variable'), ('+', 'operation'), ('x', 'variable'), ('**', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = '8 + x + y + y^3 + x^2'
        res = [('8', 'number'), ('+', 'operation'), ('x', 'variable'), ('+', 'operation'), ('y', 'variable'), ('+', 'operation'), ('y', 'variable'), ('**', 'operation'), ('3', 'number'), ('+', 'operation'), ('x', 'variable'), ('**', 'operation'), ('2', 'number')]
        self.assertEqual(parse_function(f), res)
        f = '-x**2 - 123.045'
        res = [('-', 'operation'), ('x', 'variable'), ('**', 'operation'), ('2', 'number'), ('-', 'operation'), ('123.045', 'number')]
        self.assertEqual(parse_function(f), res)
        f = '@'
        with self.assertRaises(InputError):
            parse_function(f)

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
        f = '3x+4'
        res = [('+', 'operation'), ('*', 'operation'), ('3', 'number'), ('x', 'variable'), ('4', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '3x+4+5+6+7+8'
        res = [('+', 'operation'), ('+', 'operation'), ('+', 'operation'), ('+', 'operation'), ('+', 'operation'), ('*', 'operation'), ('3', 'number'), ('x', 'variable'), ('4', 'number'), ('5', 'number'), ('6', 'number'), ('7', 'number'), ('8', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '3x+4y'
        res = [('+', 'operation'), ('*', 'operation'), ('3', 'number'), ('x', 'variable'), ('*', 'operation'), ('4', 'number'), ('y', 'variable')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '3*(2x)'
        res = [('*', 'operation'), ('3', 'number'), ('*', 'operation'), ('2', 'number'), ('x', 'variable')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = 'x^2'
        res = [('**', 'operation'), ('x', 'variable'), ('2', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '8 + x + x^2'
        res = [('+', 'operation'), ('+', 'operation'), ('8', 'number'), ('x', 'variable'), ('**', 'operation'), ('x', 'variable'), ('2', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '8 + x + y + y^3 + x^2'
        res = [('+', 'operation'), ('+', 'operation'), ('+', 'operation'), ('+', 'operation'), ('8', 'number'), ('x', 'variable'), ('y', 'variable'), ('**', 'operation'), ('y', 'variable'), ('3', 'number'), ('**', 'operation'), ('x', 'variable'), ('2', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)
        f = '5x^2y + xy^2 + y^2'
        res = [('+', 'operation'), ('+', 'operation'), ('*', 'operation'), ('*', 'operation'), ('5', 'number'), ('**', 'operation'), ('x', 'variable'), ('2', 'number'), ('y', 'variable'), ('*', 'operation'), ('x', 'variable'), ('**', 'operation'), ('y', 'variable'), ('2', 'number'), ('**', 'operation'), ('y', 'variable'), ('2', 'number')]
        self.assertEqual(order_prefix(parse_function(f)), res)

    def test_construct_expression_tree(self):
        f = '(4-x)*(5+y)'
        t = construct_expression_tree(order_prefix(parse_function(f)))
        self.assertEqual(t.left.value, '-')
        self.assertEqual(t.left.left.value, '4')
        self.assertEqual(t.left.right.value, 'x')
        self.assertEqual(t.right.left.value, '5')
        self.assertEqual(t.right.right.value, 'y')

        f = '8 + x + y + y^3 + x^2'
        t = construct_expression_tree(order_prefix(parse_function(f)))
        self.assertEqual(t.value, '+')
        self.assertEqual(t.left.value, '+')
        self.assertEqual(t.left.left.value, '+')
        self.assertEqual(t.left.left.left.value, '+')
        self.assertEqual(t.left.left.left.left.value, '8')
        self.assertEqual(t.left.left.left.right.value, 'x')
        self.assertEqual(t.left.left.right.value, 'y')
        self.assertEqual(t.left.right.value, '**')
        self.assertEqual(t.left.right.left.value, 'y')
        self.assertEqual(t.left.right.right.value, '3')
        self.assertEqual(t.right.value, '**')

        f = '3x+4'
        t = construct_expression_tree(order_prefix(parse_function(f)))
        self.assertEqual(t.value, '+')
        self.assertEqual(t.left.value, '*')
        self.assertEqual(t.right.value, '4')
        self.assertEqual(t.left.left.value, '3')
        self.assertEqual(t.left.right.value, 'x')


if __name__ == '__main__':
    unittest.main()
