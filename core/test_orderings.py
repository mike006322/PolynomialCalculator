import unittest
from orderings import *


class TestParser(unittest.TestCase):

    def test_order_lex(self):
        # -5x^3 + 7x^2z^2 + 4xy^2z + 4z^2
        term_matrix = [[' ', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
        self.assertEqual(grev_lex(term_matrix), [[' ', 'x', 'y', 'z'], [4, 1, 2, 1], [7, 2, 0, 2], [-5, 3, 0, 0], [4, 0, 0, 2]])
        ordered_reverse_lex = [[' ', 'x', 'y', 'z'], [4, 0, 0, 2], [4, 1, 2, 1], [7, 2, 0, 2], [-5, 3, 0, 0]]
        self.assertEqual(reverse_lex(term_matrix), ordered_reverse_lex)
        ordered_lex = [[' ', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
        self.assertEqual(order_lex(term_matrix), ordered_lex)
        term_matrix2 = [[' ', 'x', 'y'], [1.0, 2, 0], [1.0, 1, 0], [1.0, 0, 3], [1.0, 0, 1], [8.0, 0, 0]]
        ordered_lex2 = [[' ', 'x', 'y'], [1.0, 2, 0], [1.0, 1, 0], [1.0, 0, 3], [1.0, 0, 1], [8.0, 0, 0]]
        self.assertEqual(order_lex(term_matrix2), ordered_lex2)


if __name__ == '__main__':
    unittest.main()
