import unittest
from multivariable_polynomial import Polynomial

class TestParser(unittest.TestCase):

    def test_solve_num_of_variables(self):
        s = 'xy'
        S = Polynomial(s)
        t = '2'
        T = Polynomial(t)
        u = 'x^3+x+1'
        U = Polynomial(u)
        v = 'x^2+x+1'
        V = Polynomial(v)
        z = '3x'
        Z = Polynomial(z)
        d = '3x + 5'
        D = Polynomial(d)
        self.assertEqual(S.solve(), 'too many variables')
        self.assertEqual(T.solve(), 2)
        self.assertEqual(U.solve(), 'I cannot solve yet...')
        self.assertEqual(Z.solve(), 0)
        self.assertEqual(D.solve(), -5/3)

    s = '7x^2+8x+9'
    S = Polynomial(s)
    print(S.solve())
    # = ((-27.999999999999996+47.989582202807306j), (-28-47.989582202807306j))
    # python is rounding the answers

    def test_quadratic_formula(self):
        s = 'x^2-1'
        S = Polynomial(s)
        t = 'x^2-3x+2'
        T = Polynomial(t)
        self.assertEqual(S.solve(), 1)
        self.assertEqual(set(T.solve()), {1, 2})

if __name__ == '__main__':
    unittest.main()
