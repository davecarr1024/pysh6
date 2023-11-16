from unittest import TestCase
from pysh.pype.vals import builtins


class IntTest(TestCase):
    def test_eq(self) -> None:
        self.assertEqual(builtins.Int.create(1), builtins.Int.create(1))
        self.assertNotEqual(builtins.Int.create(1), builtins.Int.create(2))
