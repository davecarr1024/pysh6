from unittest import TestCase
from pysh import pysh


class StateTest(TestCase):
    def test_defaults(self) -> None:
        self.assertEqual(
            pysh.State().scope["int"].val,
            pysh.vals.int_class,
        )
        self.assertEqual(
            pysh.State().scope["none"].val,
            pysh.vals.none,
        )

    def test_id(self) -> None:
        self.assertIsNot(
            pysh.State(),
            pysh.State(),
        )
        self.assertIsNot(
            pysh.State().as_child(),
            pysh.State().as_child(),
        )

    def test_set(self) -> None:
        state = pysh.State().as_child()
        state["a"] = pysh.vals.Var.for_val(pysh.vals.int_(1))
        self.assertIn("a", state)
        self.assertEqual(state["a"].val, pysh.vals.int_(1))
        state = pysh.State().as_child()
        self.assertNotIn("a", state)
        state["a"] = pysh.vals.Var.for_val(pysh.vals.int_(2))
        self.assertIn("a", state)
        self.assertEqual(state["a"].val, pysh.vals.int_(2))
