from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, regex


class AndTest(TestCase):
    def test_call(self):
        for state, expected in list[tuple[regex.State, Optional[regex.StateAndResult]]](
            [
                (
                    regex.State(),
                    None,
                ),
                (
                    regex.State.load("a"),
                    None,
                ),
                (
                    regex.State.load("b"),
                    None,
                ),
                (
                    regex.State.load("ab"),
                    regex.State().and_result(regex.Result.load("ab")),
                ),
                (
                    regex.State.load("abc"),
                    regex.State.load("c", chars.Position(0, 2)).and_result(
                        regex.Result.load("ab")
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.And([regex.Literal("a"), regex.Literal("b")])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
