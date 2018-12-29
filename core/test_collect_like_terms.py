import unittest
from collect_like_terms import collect_like_terms


class TestCollectLikeTerms(unittest.TestCase):

    def test_collect_like_terms(self):
        # 'x^2y+4x^2y+8+16+2x+y = 5x^2y+2x+y+24'
        term_matrix = [[' ', 'y', 'x', 'z'], [1.0, 1, 2, 0], [4.0, 1, 2, 0], [8.0, 0, 0, 0], [16.0, 0, 0, 0], [2.0, 0, 1, 0], [1.0, 1, 0, 0]]
        term_matrix_copy = term_matrix.copy()
        self.assertEqual(collect_like_terms(term_matrix), [[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]])
        self.assertEqual(term_matrix, term_matrix_copy)
        term_matrix = [[' ', 'x'], [0.0, 1]]
        self.assertEqual(collect_like_terms(term_matrix), [[' ']])
        term_matrix = [[' ', 'x'], [1, 1], [1, 1]]
        self.assertEqual(collect_like_terms(term_matrix), [[' ', 'x'], [2, 1]])


if __name__ == '__main__':
    unittest.main()
