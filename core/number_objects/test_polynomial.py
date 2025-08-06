import unittest
from core.number_objects.polynomial import Polynomial, NonFactor, division_algorithm, division_string, divides, gcd, lcm, graded_order


class TestPolynomial(unittest.TestCase):

    def test__init__(self):
        self.assertEqual(Polynomial(0).term_matrix, [['constant']])
        t = [['constant', 'y', 'x'], [5.0, 1, 2], [24.0, 0, 0], [2.0, 0, 1], [1.0, 1, 0]]
        t = Polynomial(t, char=2)
        self.assertEqual(t.term_matrix, [['constant', 'y', 'x'], [1.0, 1, 2], [1.0, 1, 0]])

    def test_clean(self):
        self.assertEqual(Polynomial.clean([['constant', 'x', 'y'], [3.0, 2, 0], [1.0, 1, 0], [5.0, 0, 0]]), [['constant', 'x'], [3.0, 2], [1.0, 1], [5.0, 0]])

    def test___str__(self):
        self.assertEqual(Polynomial('-x^2 -1'), '-x^2 - 1')

    def test_equals(self):
        a = Polynomial(0)
        b = Polynomial('0')
        c = 0
        self.assertEqual(a, c)
        self.assertEqual(a, b)
        self.assertFalse(a != b)

    def test_addition(self):
        a = Polynomial('x')
        b = Polynomial(0)
        self.assertTrue(a + b == a)
        self.assertTrue(a + 0 == a)
        self.assertTrue('x' + a == Polynomial('2x'))
        a = Polynomial('x', char=2)
        self.assertTrue(a + a == 0)
        self.assertEqual(Polynomial('x^2-x') + 'x', Polynomial('x^2'))

    def test_subtraction(self):
        a = Polynomial('x + 1')
        b = Polynomial(1)
        c = Polynomial('x')
        self.assertTrue(a - b == c)
        a = Polynomial('x', char=2)
        self.assertTrue(a - a == 0)
        a = Polynomial('3x + 1', char=2)
        b = Polynomial('x + 1', char=2)
        self.assertTrue(a - b == 0)

    def test_multiplication(self):
        a = Polynomial('x')
        b = Polynomial(2)
        c = Polynomial('2x')
        self.assertTrue(a * b == c)
        self.assertTrue('x' * b == c)
        self.assertTrue(a * 2 == c)
        a = Polynomial('x', char=2)
        b = Polynomial(2, char=2)
        self.assertTrue(a * b == 0)

    def test_pow(self):
        x = Polynomial('x')
        self.assertEqual(x**2, Polynomial('x^2'))

    def test_division(self):
        t = Polynomial('xy - 1')
        s = Polynomial('y^2 - 1')
        a = Polynomial('x^2 - 1')
        b = Polynomial('x + 1')
        c = Polynomial('x - 1')
        self.assertTrue(a / b == c)
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertTrue(b / b == 1)
        self.assertRaises(NonFactor, lambda: t / s)
        a = Polynomial('2x^2 - 2', char=2)
        b = Polynomial('x + 1', char=2)
        self.assertTrue(a / b == 0)

    def test_LT(self):
        t = Polynomial('xy - 1')
        s = Polynomial('x^2y + xy^2 + y^2')
        self.assertEqual(t.LT(), Polynomial('xy'))
        self.assertEqual(s.LT(), Polynomial('x^2y'))
        self.assertEqual(Polynomial('0').LT(), 0)

    def test_LM(self):
        t = Polynomial('3xy - 1')
        s = Polynomial('5x^2y + xy^2 + y^2')
        self.assertEqual(t.LM(), Polynomial('xy'))
        self.assertEqual(s.LM(), Polynomial('x^2y'))
        self.assertEqual(Polynomial('0').LM(), 0)

    def test_terms(self):
        s = Polynomial('5x^2y + xy^2 + y^2')
        self.assertEqual(list(s.terms()), [Polynomial('5x^2y'), Polynomial('xy^2'), Polynomial('y^2')])

    def test__iter__(self):
        S = Polynomial('x^2y + xy^2 + y^2')
        self.assertEqual([term for term in S], [Polynomial('x^2y'), Polynomial('xy^2'), Polynomial('y^2')])

    def test_mod_char(self):
        t = [['constant', 'y', 'x'], [5, 1, 2], [24, 0, 0], [2, 0, 1], [1, 1, 0]]
        t = Polynomial(t, char=2)
        self.assertEqual(t.term_matrix, [['constant', 'y', 'x'], [1, 1, 2], [1, 1, 0]])

    def test_combine_variables(self):
        t = Polynomial('x')
        s = Polynomial('x^2y + xy^2 + y^2')
        res = (Polynomial([['constant', 'x', 'y'], [1, 2, 1], [1, 1, 2], [1, 0, 2]]), Polynomial([['constant', 'x', 'y'], [1, 1, 0]]))
        self.assertEqual(Polynomial.combine_variables(s, t), res)
        self.assertEqual(s.term_matrix, [['constant', 'x', 'y'], [1, 2, 1], [1, 1, 2], [1, 0, 2]])
        self.assertEqual(t.term_matrix, [['constant', 'x'], [1, 1]])

    def test_mod(self):
        self.assertEqual(Polynomial('x^2y + xy^2 + y^2') % Polynomial('x'), Polynomial('y^2'))
        self.assertEqual(Polynomial('x^2y + xy^2 + y^2') % 'x', Polynomial('y^2'))
        # self.assertEqual('x^2y + xy^2 + y^2' % Polynomial('x'), Polynomial('y^2'))
        # __rmod__ cannot override the string's LHS __mod__ operator, see bug at: https://bugs.python.org/issue28598

    def test_degree(self):
        self.assertEqual(Polynomial('x + x^2').degree(), 2)
        self.assertEqual(Polynomial('8 + x + x^2').degree(), 2)
        self.assertEqual(Polynomial('8 + x + y + y^3 + x^2').degree(), 3)
        self.assertEqual(Polynomial('8 + x + y + y^3x^3 + x^2').degree(), 6)

    def test_variables(self):
        self.assertEqual(Polynomial('2x^3+x+8').variables, ['x'])
        self.assertEqual(Polynomial('2x^3+xy+8').variables, ['x', 'y'])

    def test_number_of_variables(self):
        self.assertEqual(Polynomial('2x^3+x+8').number_of_variables, 1)
        self.assertEqual(Polynomial('2x^3+xy+8').number_of_variables, 2)

    def test_division_algorithm(self):
        s = Polynomial('x^2y + xy^2 + y^2')
        t = Polynomial('xy - 1')
        e = Polynomial('y^2 - 1')
        res1 = ([Polynomial('x + y'), Polynomial('1')], Polynomial('x + y + 1.0'))
        res2 = ([Polynomial('xy + y^2'), Polynomial('y')], Polynomial('0'))
        self.assertEqual(res1, division_algorithm(s, t, e))
        self.assertEqual(res2, division_algorithm(s, Polynomial('x'), Polynomial('y')))

    def test_division_string(self):
        s = Polynomial('x^2y + xy^2 + y^2')
        t = Polynomial('xy - 1')
        e = Polynomial('y^2 - 1')
        res1 = 'x^2y + xy^2 + y^2 = (x + y)*(xy - 1.0) + (1.0)*(y^2 - 1.0) + (remainder:) x + y + 1.0'
        res2 = 'x^2y + xy^2 + y^2 = (xy + y^2)*(x) + (y)*(y) + (remainder:) 0'
        self.assertEqual(res1, division_string(s, t, e))
        self.assertEqual(res2, division_string(s, Polynomial('x'), Polynomial('y')))

    def test_divides(self):
        t = Polynomial('xy - 1')
        s = Polynomial('x^2y + xy^2 + y^2')
        self.assertEqual(divides(t, s), True)
        self.assertEqual(divides(s, t), False)

    def test_isolate_variable(self):
        s = Polynomial('x^2y + xy^2 + y^2')
        tm = [['constant', 'y'], [Polynomial([['constant', 'x'], [1, 2]]), 1], [Polynomial([['constant', 'x'], [1, 1], [1, 0]]), 2]]
        self.assertEqual(s.isolate('y').term_matrix, tm)
        # print(Polynomial('xyz+z+z^2').isolate('z'))
        # print(Polynomial('x').isolate('y'))

    def test_gcd(self):
        self.assertEqual(gcd(Polynomial('2x'), Polynomial('2')), 2)
        self.assertEqual(gcd(Polynomial('x^2-1'), Polynomial('x-1')), Polynomial('x + -1.0'))
        self.assertEqual(gcd(Polynomial('x-1'), Polynomial('x^2-1')), Polynomial('x + -1.0'))
        self.assertEqual(gcd(Polynomial('x', 2)**2 - Polynomial('x', 2), Polynomial('x^3 + x + 1', 2)), 1)
        self.assertEqual(gcd(Polynomial('x^4 + x^2 + 1.0', 2), Polynomial('x^4-x', 2)), Polynomial('x^2 + x + 1.0'))
        self.assertEqual(gcd(Polynomial('x', 2)**(2**3) - Polynomial('x', 2), Polynomial('x^5 + x^3 + 1.0', 2)), 1)
        self.assertEqual(gcd(Polynomial('x^2-2x+1'), Polynomial('x^2-1')) % Polynomial('x-1').degree(), 0)
        # print(gcd(Polynomial('x^3y^2'), Polynomial('x^4y')).term_matrix)
        self.assertEqual(gcd(Polynomial('x^3y^2'), Polynomial('x^4y')), Polynomial('x^3y'))

    def test_lcm(self):
        self.assertEqual(lcm(Polynomial('x^3y^2'), Polynomial('x^4y')), Polynomial('x^4y^2'))

    def test_orderings(self):
        f = Polynomial('xy+x^2+xz+y^2+yz+z^2+x+y+z+1')
        f.term_matrix = graded_order(f.term_matrix)
        g = Polynomial([['constant', 'x', 'y', 'z'], [1, 2, 0, 0], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 2, 0], [1, 0, 1, 1], [1, 0, 0, 2], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0]])
        self.assertEqual(f, g)

    def test__call__(self):
        f = Polynomial('xy+x^2+xz+y^2+yz+z^2+x+y+z+1')
        self.assertEqual(f(1, 2, 3), 32)
        g = Polynomial('2x^2+3y')
        self.assertEqual(g(2, 3), 17)
        self.assertEqual(g(2, 'y'), Polynomial('8 + 3y'))
        self.assertEqual(g(x=2), Polynomial('8 + 3y'))
        variables = {'x': 2, 'y': 1}
        self.assertEqual(g(**variables), 11)
        variables = {'x': 2}
        self.assertEqual(g(**variables), Polynomial('8 + 3y'))
        variables = {'x': 2, 'z': 4}
        self.assertEqual(g(**variables), Polynomial('8 + 3y'))
        f = Polynomial('x^2')
        res = Polynomial('a^2')
        self.assertEqual(f(Polynomial('a')), res)
        f = Polynomial('x^2y')
        res = Polynomial('a^2y')
        self.assertEqual(f(Polynomial('a'), Polynomial('y')), res)

    def test_derivative(self):
        f = Polynomial('x^2')
        self.assertEqual(f.derivative(), Polynomial('2x'))
        f = Polynomial('x^2y + y^3 + xy^3')
        self.assertEqual(f.derivative('x'), Polynomial('2xy + y^3'))
        self.assertEqual(f.derivative('y'), Polynomial('x^2 + 3xy^2 + 3y^2'))

    def test_gradient(self):
        f = Polynomial('x^2y + y^3 + xy^3')
        self.assertEqual(f.grad, [Polynomial('2xy + y^3'), Polynomial('x^2 + 3xy^2 + 3y^2')])
        self.assertEqual(f.grad(x=1, y=2), [12, 25])
        f = Polynomial('x^2')
        self.assertEqual(f.grad(1), [2])

    def test_hessian(self):
        f = Polynomial('x^2y + y^3 + xy^3')
        h = f.hessian
        self.assertEqual(h[0][0], Polynomial('2y'))
        self.assertEqual(h[0][1], Polynomial('2x + 3y^2'))
        self.assertEqual(h[1][0], Polynomial('2x + 3y^2'))
        self.assertEqual(h[1][1], Polynomial('6xy + 6y'))
        self.assertEqual(f.hessian(x=1, y=2), [[4, 14], [14, 24]])


if __name__ == '__main__':
    unittest.main()
