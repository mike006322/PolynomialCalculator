import unittest
from polynomial import Polynomial


class TestParser(unittest.TestCase):

    def test_solve_num_of_variables(self):
        s = Polynomial('xy')
        t = Polynomial('2')
        u = Polynomial('x^3+x+1')
        # v = Polynomial('x^2+x+1')
        z = Polynomial('3x')
        d = Polynomial('3x + 5')
        self.assertEqual(s.solve(), 'too many variables')
        self.assertEqual(t.solve(), 2)
        self.assertEqual(u.solve(), 'I cannot solve yet...')
        self.assertEqual(z.solve(), 0)
        self.assertEqual(d.solve(), -5/3)

    s = Polynomial('7x^2+8x+9')
    # print(s.solve())
    # = ((-27.999999999999996+47.989582202807306j), (-28-47.989582202807306j))
    # python is rounding the answers

    def test_quadratic_formula(self):
        s = Polynomial('x^2-1')
        t = Polynomial('x^2-3x+2')
        self.assertEqual(s.solve(), 1)
        self.assertEqual(set(t.solve()), {1, 2})


if __name__ == '__main__':
    unittest.main()
