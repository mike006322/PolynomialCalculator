import unittest
from number_objects.polynomial import Polynomial


class TestFormulas(unittest.TestCase):

    def test_solve_num_of_variables(self):
        s = Polynomial('xy')
        t = Polynomial('2')
        # v = Polynomial('x^2+x+1')
        z = Polynomial('3x')
        d = Polynomial('3x + 5')
        self.assertEqual(s.solve(), 'too many variables')
        self.assertEqual(t.solve(), 2)
        self.assertEqual(z.solve(), 0)
        self.assertEqual(d.solve(), -5/3)

    s = Polynomial('7x^2+8x+9')
    # print(s.solve())
    # = ((-27.999999999999996+47.989582202807306j), (-28-47.989582202807306j))
    # python is rounding the answers

    def test_quadratic_formula(self):
        r = Polynomial('x^2-1')
        s = Polynomial('x^2-3x+2')
        t = Polynomial('3x^2 + 5x')
        self.assertEqual(set(r.solve()), {1, -1})
        self.assertEqual(set(s.solve()), {1, 2})
        self.assertEqual(t.solve(), (0, -1.6666666666666667))

    def test_durand_kerner(self):
        s = Polynomial('x^2-3x+2')
        self.assertEqual(set(s.solve()), {1+0j, 2+0j})
        f = Polynomial('x^3+10x^2+169x')
        print(set(f.solve()))
        self.assertEqual(set(f.solve()), {-5-12j, -5+12j, 0j})
        # f2 = Polynomial('2y^4 + 7y^2 + 3y + 2')
        # f2 = Polynomial('2y^4')
        # The above two polynomials have solutions that are reflections over the axes
        # This causes Durand Kerner to swap the solutions with each iteration
        # print(f2.solve())
        f = Polynomial('-x^3') # this fails
        # print(f.solve())


if __name__ == '__main__':
    unittest.main()
