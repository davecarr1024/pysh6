from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, regex


class ZeroOrOneTest(TestCase):
    def test_call(self):
        for state, expected in list[tuple[regex.State, Optional[regex.StateAndResult]]](
            [
                (
                    regex.State(),
                    regex.State().and_result(""),
                ),
                (
                    regex.State.load("b"),
                    regex.State.load("b").and_result(""),
                ),
                (
                    regex.State.load("a"),
                    regex.State().and_result("a"),
                ),
                (
                    regex.State.load("aa"),
                    regex.State.load("a", chars.Position(0, 1)).and_result("a"),
                ),
                (
                    regex.State.load("ab"),
                    regex.State.load("b", chars.Position(0, 1)).and_result("a"),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.ZeroOrOne(regex.Literal("a"))
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
