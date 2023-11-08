from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, regex


class OneOrMoreTest(TestCase):
    def test_call(self):
        for state, expected in list[tuple[regex.State, Optional[regex.StateAndResult]]](
            [
                (
                    regex.State(),
                    None,
                ),
                (
                    regex.State.load("b"),
                    None,
                ),
                (
                    regex.State.load("a"),
                    regex.State().and_result("a"),
                ),
                (
                    regex.State.load("ab"),
                    regex.State.load("b", chars.Position(0, 1)).and_result("a"),
                ),
                (
                    regex.State.load("aa"),
                    regex.State().and_result("aa"),
                ),
                (
                    regex.State.load("aab"),
                    regex.State.load("b", chars.Position(0, 2)).and_result("aa"),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.OneOrMore(regex.Literal("a"))
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
