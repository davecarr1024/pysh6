from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, regex


class RangeTest(TestCase):
    def test_ctor_fail(self):
        for start, end in list[tuple[str, str]](
            [
                (
                    "",
                    "",
                ),
                (
                    "a",
                    "",
                ),
                (
                    "",
                    "b",
                ),
                (
                    "a",
                    "bb",
                ),
                (
                    "aa",
                    "b",
                ),
                (
                    "aa",
                    "bb",
                ),
            ]
        ):
            with self.subTest(start=start, end=end):
                with self.assertRaises(errors.Error):
                    regex.Range(start, end)

    def test_call(self):
        for state, expected in list[tuple[regex.State, Optional[regex.StateAndResult]]](
            [
                (
                    regex.State(),
                    None,
                ),
                (
                    regex.State.load("1"),
                    None,
                ),
                (
                    regex.State.load("a"),
                    regex.State().and_result(regex.Result.load("a")),
                ),
                (
                    regex.State.load("z"),
                    regex.State().and_result(regex.Result.load("z")),
                ),
                (
                    regex.State.load("ab"),
                    regex.State.load("b", chars.Position(0, 1)).and_result(
                        regex.Result.load("a")
                    ),
                ),
                (
                    regex.State.load("zb"),
                    regex.State.load("b", chars.Position(0, 1)).and_result(
                        regex.Result.load("z")
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = regex.Range("a", "z")
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
