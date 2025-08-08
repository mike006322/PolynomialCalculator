import unittest
from polynomials.display import set_display_mode, get_display_mode, format_number, display_mode
from polynomials.primitives.polycalc_numbers import Integer, Rational


class TestDisplay(unittest.TestCase):
    def tearDown(self):
        set_display_mode('float')

    def test_rational_mode_numbers(self):
        set_display_mode('rational')
        self.assertEqual(format_number(Integer(1)), '1')
        self.assertEqual(format_number(Rational(3, 2)), '3/2')
        self.assertEqual(format_number(2.0), '2')
        self.assertEqual(format_number(2.5), '2.5')

    def test_float_mode_numbers(self):
        set_display_mode('float')
        self.assertEqual(format_number(Integer(1)), '1.0')
        self.assertEqual(format_number(Rational(3, 2)), '1.5')
        self.assertEqual(format_number(2.0), '2.0')

    def test_context_manager(self):
        set_display_mode('float')
        with display_mode('rational'):
            self.assertEqual(get_display_mode(), 'rational')
            self.assertEqual(format_number(Integer(2)), '2')
        self.assertEqual(get_display_mode(), 'float')


if __name__ == '__main__':
    unittest.main()
