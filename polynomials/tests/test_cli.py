import sys
import subprocess
import unittest


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
        self.assertIn('x = 1.0', out)
        self.assertIn('y = 2.0', out)
        self.assertIn('z = 3.0', out)


if __name__ == '__main__':
    unittest.main()
