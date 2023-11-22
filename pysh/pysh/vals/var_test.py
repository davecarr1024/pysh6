from unittest import TestCase
from pysh import core

from pysh.pysh import vals


class VarTest(TestCase):
    def test_for_val(self) -> None:
        self.assertEqual(
            vals.Var.for_val(vals.int_(1)),
            vals.Var(
                vals.int_class,
                vals.int_(1),
            ),
        )

    def test_initialized(self) -> None:
        self.assertFalse(vals.Var(vals.int_class).initialized)
        self.assertTrue(vals.Var.for_val(vals.int_(1)).initialized)

    def test_ctor_type_error(self) -> None:
        with self.assertRaises(core.errors.Error):
            vals.Var(vals.int_class, vals.none)

    def test_get(self) -> None:
        with self.assertRaises(core.errors.Error):
            vals.Var(vals.int_class).val
        self.assertEqual(vals.Var.for_val(vals.int_(1)).val, vals.int_(1))

    def test_set_empty(self) -> None:
        var = vals.Var(vals.int_class)
        var.val = vals.int_(1)
        self.assertEqual(var.val, vals.int_(1))

    def test_set_nonempty(self) -> None:
        var = vals.Var.for_val(vals.int_(1))
        self.assertEqual(var.val, vals.int_(1))
        var.val = vals.int_(2)
        self.assertEqual(var.val, vals.int_(2))

    def test_set_fail(self) -> None:
        var = vals.Var.for_val(vals.none)
        with self.assertRaises(core.errors.Error):
            var.val = vals.int_(1)
