import unittest
from polynomials.orderings import order_lex, order_grevlex, order_lexdeg, order_grevlexdeg, reverse_lex


class TestOrderings(unittest.TestCase):

    def test_order_lex(self):
        term_matrix = [['constant', 'a', 'y', 'z'], [-5, 3, 0, 0]]
        res = [['constant', 'a', 'y', 'z'], [-5, 3, 0, 0]]
        self.assertEqual(order_lex(term_matrix), res)
        # -5x^3 + 7x^2z^2 + 4xy^2z + 4z^2
        term_matrix1 = [['constant', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
        res1 = [['constant', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
        self.assertEqual(order_lex(term_matrix1), res1)
        term_matrix2 = [['constant', 'x', 'y'], [1.0, 2, 0], [1.0, 1, 0], [1.0, 0, 3], [1.0, 0, 1], [8.0, 0, 0]]
        res2 = [['constant', 'x', 'y'], [1.0, 2, 0], [1.0, 1, 0], [1.0, 0, 3], [1.0, 0, 1], [8.0, 0, 0]]
        self.assertEqual(order_lex(term_matrix2), res2)

    def test_reverse_lex(self):
        # -5x^3 + 7x^2z^2 + 4xy^2z + 4z^2
        term_matrix = [['constant', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
        res = [['constant', 'x', 'y', 'z'], [7, 2, 0, 2], [4, 0, 0, 2], [4, 1, 2, 1], [-5, 3, 0, 0]]
        self.assertEqual(reverse_lex(term_matrix), res)
    #
    # def test_grev_lex(self):
    #     # -5x^3 + 7x^2z^2 + 4xy^2z + 4z^2
    #     term_matrix = [['constant', 'x', 'y', 'z'], [-5, 3, 0, 0], [7, 2, 0, 2], [4, 1, 2, 1], [4, 0, 0, 2]]
    #     res = [['constant', 'x', 'y', 'z'], [4, 1, 2, 1], [7, 2, 0, 2], [-5, 3, 0, 0], [4, 0, 0, 2]]
    #     self.assertEqual(grev_lex(term_matrix), res)


if __name__ == '__main__':
    unittest.main()
