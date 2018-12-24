import unittest
import poly_parser


class TestParser(unittest.TestCase):

    def test_findVars(self):
        """
        Input is a list of terms after replace(" ", "").replace("-","+-").replace("*", "").lower().split("+"),
        Output is a set of discovered variables
        """
        self.assertEqual(poly_parser.findVars(['x', 'y', 'z']), {'x', 'y', 'z'})
        self.assertEqual(poly_parser.findVars(['x1^2x2^3', '-9z^4t^2', '7x^2x2^6']), {'x2', 'z', 't', 'x', 'x1'})

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
