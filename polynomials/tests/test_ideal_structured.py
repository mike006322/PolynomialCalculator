import unittest
from polynomials.ideal import Ideal
from polynomials.polynomial import Polynomial


class TestIdealStructuredSolutions(unittest.TestCase):
    def test_structured_single_solution(self):
        # x^2 = 0, y = 0, z = 0 → single solution at (0,0,0)
        f1 = Polynomial('x^2')
        f2 = Polynomial('y')
        f3 = Polynomial('z')
        I = Ideal(f1, f2, f3)
        sols = I.solve_system_structured()
        self.assertIsInstance(sols, list)
        self.assertEqual(len(sols), 1)
        sol = sols[0]
        # Keys present and numeric types
        self.assertEqual(set(sol.keys()), {'x', 'y', 'z'})
        self.assertAlmostEqual(sol['x'], 0.0)
        self.assertEqual(sol['y'], 0)
        self.assertEqual(sol['z'], 0)

    def test_structured_specific_point(self):
        # System with unique solution x=1, y=2, z=3
        f1 = Polynomial('x-1')
        f2 = Polynomial('y-2')
        f3 = Polynomial('z-3')
        I = Ideal(f1, f2, f3)
        sols = I.solve_system_structured()
        self.assertEqual(len(sols), 1)
        sol = sols[0]
        self.assertAlmostEqual(sol['x'], 1.0)
        self.assertAlmostEqual(sol['y'], 2.0)
        self.assertAlmostEqual(sol['z'], 3.0)

    def test_structured_infinite_or_undetermined(self):
        # This fails the solvability criteria (not finite solutions)
        f1 = Polynomial('xy')
        f2 = Polynomial('y')
        I = Ideal(f1, f2)
        sols = I.solve_system_structured()
        self.assertIsNone(sols)


if __name__ == '__main__':
    unittest.main()
