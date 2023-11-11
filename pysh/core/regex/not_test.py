from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, regex


class NotTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                regex.State,
                Optional[regex.StateAndResult],
            ]
        ](
            [
                (
                    regex.State.load("a"),
                    None,
                ),
                (
                    regex.State.load("b"),
                    regex.StateAndResult(
                        regex.State(),
                        regex.Result.load("b"),
                    ),
                ),
                (
                    regex.State.load("ba"),
                    regex.StateAndResult(
                        regex.State.load("a", chars.Position(0, 1)),
                        regex.Result.load("b"),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.Not(regex.Literal("a"))
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    actual = rule(state)
                    self.assertEqual(
                        actual,
                        expected,
                        f"actual {actual} != expected {expected}",
                    )
