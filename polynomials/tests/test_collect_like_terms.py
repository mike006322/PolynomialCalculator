import unittest

from polynomials.collect_like_terms import collect_like_terms


class TestCollectLikeTerms(unittest.TestCase):

    def test_collect_like_terms(self):
        # 'x^2y+4x^2y+8+16+2x+y = 5x^2y+2x+y+24'
        term_matrix = [
            ["constant", "y", "x", "z"],
            [1.0, 1, 2, 0],
            [4.0, 1, 2, 0],
            [8.0, 0, 0, 0],
            [16.0, 0, 0, 0],
            [2.0, 0, 1, 0],
            [1.0, 1, 0, 0],
        ]
        term_matrix_copy = term_matrix.copy()
        # Default: preserve_header=True, so header is preserved as-is (including unused 'z')
        self.assertEqual(
            collect_like_terms(term_matrix),
            [
                ["constant", "y", "x", "z"],
                [5.0, 1, 2, 0],
                [24.0, 0, 0, 0],
                [2.0, 0, 1, 0],
                [1.0, 1, 0, 0],
            ],
        )
        # If preserve_header=False, unused variables are removed
        self.assertEqual(
            collect_like_terms(term_matrix, preserve_header=False),
            [[5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]],
        )
        self.assertEqual(term_matrix, term_matrix_copy)
        term_matrix = [["constant", "x"], [0.0, 1]]
        self.assertEqual(collect_like_terms(term_matrix), [["constant"]])
        term_matrix = [["constant", "x"], [1, 1], [1, 1]]
        self.assertEqual(collect_like_terms(term_matrix), [["constant", "x"], [2, 1]])


if __name__ == "__main__":
    unittest.main()
