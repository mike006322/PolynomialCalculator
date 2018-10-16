import unittest
import collect_like_terms

class TestParser(unittest.TestCase):

    def test_collect_like_terms(self):
        # 'x^2y+4x^2y+8+16+2x+y = 5x^2y+2x+y+24'
        termMatrix = [[' ', 'y', 'x', 'z'], [1.0, 1, 2, 0], [4.0, 1, 2, 0], [8.0, 0, 0, 0], [16.0, 0, 0, 0], [2.0, 0, 1, 0], [1.0, 1, 0, 0]]
        self.assertEqual(collect_like_terms.collect_like_terms(termMatrix), [[' ', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]])

if __name__ == '__main__':
    unittest.main()
