import sys
import subprocess
import unittest
import json


def run_cli(args):
    # Run via module to ensure imports work from source checkout
    cmd = [sys.executable, '-m', 'polynomials.cli.cli'] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout, res.stderr


class TestCLI(unittest.TestCase):
    def test_version(self):
        code, out, err = run_cli(['--version'])
        self.assertEqual(code, 0)
        self.assertIn('polycalc', out)
        self.assertNotIn('unknown', out)

    def test_groebner_order_variants(self):
        # Small system where ordering affects intermediate LM; just check it runs and prints header
        code, out, err = run_cli(['groebner', 'x^2+y^2-1', 'x-y', '--order', 'lex'])
        self.assertEqual(code, 0)
        self.assertIn('Groebner basis:', out)

        code, out, err = run_cli(['groebner', 'x^2+y^2-1', 'x-y', '--order', 'grlex'])
        self.assertEqual(code, 0)
        self.assertIn('Groebner basis:', out)

        code, out, err = run_cli(['groebner', 'x^2+y^2-1', 'x-y', '--order', 'grevlex'])
        self.assertEqual(code, 0)
        self.assertIn('Groebner basis:', out)

    def test_solve_system_structured_cli(self):
        code, out, err = run_cli(['solve-system', 'x-1', 'y-2', 'z-3'])
        self.assertEqual(code, 0)
        self.assertIn('1 solutions:', out)
        self.assertIn('x = 1.0', out)  # default may be float prior to display mode flags

    def test_json_solve(self):
        code, out, err = run_cli(['--json', 'solve', 'x^2-2', 'x'])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload.get('command'), 'solve')
        self.assertEqual(payload.get('status'), 'ok')
        self.assertIsInstance(payload.get('solutions'), list)
        self.assertEqual(payload.get('count'), len(payload.get('solutions')))

    def test_json_solve_system(self):
        code, out, err = run_cli(['--json', 'solve-system', 'x-1', 'y-2'])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload.get('command'), 'solve-system')
        self.assertIn(payload.get('status'), ['ok', 'no_solutions', 'undetermined'])
        if payload.get('status') == 'ok':
            self.assertEqual(payload.get('count'), len(payload.get('solutions')))
            self.assertIsInstance(payload.get('solutions'), list)
            self.assertTrue(all(isinstance(s, dict) for s in payload.get('solutions')))

    def test_json_groebner(self):
        code, out, err = run_cli(['--json', 'groebner', 'x^2+y^2-1', 'x-y', '--order', 'grevlex'])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload.get('command'), 'groebner')
        self.assertEqual(payload.get('status'), 'ok')
        self.assertIsInstance(payload.get('basis'), list)

    def test_json_failure_invalid_poly(self):
        # Provide an invalid polynomial to trigger runtime error in JSON mode
        code, out, err = run_cli(['--json', 'solve', 'x^2+-', 'x'])
        self.assertEqual(code, 1)
        # Should still emit JSON payload about the error
        payload = json.loads(out)
        self.assertEqual(payload.get('status'), 'error')
        self.assertIn('error', payload)

    def test_numeric_output_flags_solve_system(self):
        # Rational mode: integers should not have .0
        code, out, err = run_cli(['--rational', 'solve-system', 'x-1', 'y-2'])
        self.assertEqual(code, 0)
        self.assertIn('x = 1', out)
        self.assertIn('y = 2', out)
        self.assertNotIn('1.0', out)
        self.assertNotIn('2.0', out)
        # Float mode: integers should display with .0
        code, out, err = run_cli(['--float', 'solve-system', 'x-1', 'y-2'])
        self.assertEqual(code, 0)
        self.assertIn('x = 1.0', out)
        self.assertIn('y = 2.0', out)

    def test_numeric_output_flags_groebner(self):
        # Rational mode should drop .0 in integer constants
        code, out, err = run_cli(['--rational', 'groebner', 'x^2+y^2-1', 'x-y', '--order', 'grevlex'])
        self.assertEqual(code, 0)
        self.assertIn('Groebner basis:', out)
        self.assertIn('x - y', out)
        self.assertIn('2y^2 - 1', out)
        self.assertNotIn('2.0', out)
        self.assertNotIn('1.0', out)
        # Float mode should include .0 for integer-looking floats
        code, out, err = run_cli(['--float', 'groebner', 'x^2+y^2-1', 'x-y', '--order', 'grevlex'])
        self.assertEqual(code, 0)
        self.assertIn('Groebner basis:', out)
        self.assertIn('x - y', out)
        self.assertIn('2.0y^2 - 1.0', out)


if __name__ == '__main__':
    unittest.main()
