import unittest
from variable import Variable


class TestVector(unittest.TestCase):

    def test__init__(self):
        x = Variable('x')
        self.assertEqual(repr(x), 'x')
        self.assertEqual(str(x), 'x')


if __name__ == '__main__':
    unittest.main()
