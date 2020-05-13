import unittest

from FonctionBD import is_number

class MyTest(unittest.TestCase):
    def test_number(self):
        self.assertTrue(is_number(5))
        self.assertTrue(is_number("3643483"))
        self.assertTrue(is_number(5.530))
        self.assertFalse(is_number("5,530"))
        self.assertFalse(is_number("treize"))


if __name__ == '__main__':
    unittest.main()