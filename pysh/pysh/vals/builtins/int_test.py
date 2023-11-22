from unittest import TestCase
from pysh import pysh


class IntTest(TestCase):
    def test_ctor(self):
        pysh.vals.int_(1)

    def test_eq(self):
        self.assertEqual(pysh.vals.int_(1), pysh.vals.int_(1))
        self.assertNotEqual(pysh.vals.int_(1), pysh.vals.int_(2))

    def test_class_eq(self) -> None:
        self.assertEqual(
            pysh.vals.int_class,
            pysh.vals.int_class,
        )
        self.assertNotEqual(
            pysh.vals.int_class,
            pysh.vals.none_class,
        )

    def test_class_in_ancestors(self) -> None:
        self.assertIn(
            pysh.vals.int_class,
            pysh.vals.int_class.ancestors,
        )

    def test_class_name(self) -> None:
        self.assertEqual(pysh.vals.int_class.name, "int")
