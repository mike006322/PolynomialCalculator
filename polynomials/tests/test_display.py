import os
import unittest

from polynomials.display import display_mode, format_number, get_display_mode, set_display_mode
from polynomials.primitives.polycalc_numbers import Integer, Rational


class TestDisplay(unittest.TestCase):
    def tearDown(self):
        set_display_mode("float")

    def test_rational_mode_numbers(self):
        set_display_mode("rational")
        self.assertEqual(format_number(Integer(1)), "1")
        self.assertEqual(format_number(Rational(3, 2)), "3/2")
        self.assertEqual(format_number(2.0), "2")
        self.assertEqual(format_number(2.5), "2.5")

    def test_float_mode_numbers(self):
        set_display_mode("float")
        self.assertEqual(format_number(Integer(1)), "1.0")
        self.assertEqual(format_number(Rational(3, 2)), "1.5")
        self.assertEqual(format_number(2.0), "2.0")

    def test_context_manager(self):
        set_display_mode("float")
        with display_mode("rational"):
            self.assertEqual(get_display_mode(), "rational")
            self.assertEqual(format_number(Integer(2)), "2")
        self.assertEqual(get_display_mode(), "float")

    def test_env_variable_initialization(self):
        # Simulate setting env var before import by reloading module
        import importlib

        import polynomials.display as disp

        set_display_mode("float")
        os.environ["POLYCALC_NUMERIC_OUTPUT"] = "rational"
        importlib.reload(disp)
        self.assertEqual(disp.get_display_mode(), "rational")
        # Cleanup: restore
        os.environ.pop("POLYCALC_NUMERIC_OUTPUT", None)
        importlib.reload(disp)
        self.assertEqual(disp.get_display_mode(), "float")


if __name__ == "__main__":
    unittest.main()
