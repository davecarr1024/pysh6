from typing import Optional
from unittest import TestCase
from pysh.core import errors, regex


class NotInTest(TestCase):
    def test_call(self) -> None:
        for state, expected in list[
            tuple[
                regex.State,
                Optional[regex.StateAndResult],
            ]
        ](
            [
                (
                    regex.State(),
                    regex.StateAndResult(
                        regex.State(),
                        regex.Result(),
                    ),
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
                    regex.State.load("c"),
                    regex.StateAndResult(
                        regex.State(),
                        regex.Result.load("c"),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.NotIn(regex.ZeroOrMore(regex.Any()), ["a", "b"])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
