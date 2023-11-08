from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, regex


class OrTest(TestCase):
    def test_call(self):
        for state, expected in list[tuple[regex.State, Optional[regex.StateAndResult]]](
            [
                (
                    regex.State(),
                    None,
                ),
                (
                    regex.State.load("c"),
                    None,
                ),
                (
                    regex.State.load("a"),
                    regex.State().and_result("a"),
                ),
                (
                    regex.State.load("b"),
                    regex.State().and_result("b"),
                ),
                (
                    regex.State.load("ac"),
                    regex.State.load("c", chars.Position(0, 1)).and_result("a"),
                ),
                (
                    regex.State.load("bc"),
                    regex.State.load("c", chars.Position(0, 1)).and_result("b"),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.Or([regex.Literal("a"), regex.Literal("b")])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
