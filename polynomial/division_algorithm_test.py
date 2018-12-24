import unittest
from polynomial import Polynomial
from division_algorithm import division_algorithm
from division_algorithm import division_string
from division_algorithm import divides


class TestParser(unittest.TestCase):

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
        res1 = 'x^2y + xy^2 + y^2 = (x + y)*(xy + -1.0) + (1.0)*(y^2 + -1.0) + (remainder:) x + y + 1.0'
        res2 = 'x^2y + xy^2 + y^2 = (xy + y^2)*(x) + (y)*(y) + (remainder:) 0'
        self.assertEqual(res1, division_string(s, t, e))
        self.assertEqual(res2, division_string(s, Polynomial('x'), Polynomial('y')))

    def test_divides(self):
        t = Polynomial('xy - 1')
        s = Polynomial('x^2y + xy^2 + y^2')
        self.assertEqual(divides(t, s), True)
        self.assertEqual(divides(s, t), False)


if __name__ == '__main__':
    unittest.main()


