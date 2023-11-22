from unittest import TestCase
from pysh import pysh


class IntTest(TestCase):
    def test_ctor(self):
        pysh.vals.int_(1)

    def test_eq(self):
        self.assertEqual(pysh.vals.int_(1), pysh.vals.int_(1))
        self.assertNotEqual(pysh.vals.int_(1), pysh.vals.int_(2))
