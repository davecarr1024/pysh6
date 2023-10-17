from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors
from pysh.core.regex.result import Result


class ResultTest(TestCase):
    def test_bool(self):
        for result, expected in list[tuple[Result, bool]](
            [
                (
                    Result(),
                    False,
                ),
                (
                    Result([chars.Char("a")]),
                    True,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(bool(result), expected)

    def test_len(self):
        for result, expected in list[tuple[Result, int]](
            [
                (
                    Result(),
                    0,
                ),
                (
                    Result([chars.Char("a")]),
                    1,
                ),
                (
                    Result(
                        [
                            chars.Char("a"),
                            chars.Char("b"),
                        ]
                    ),
                    2,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(len(result), expected)

    def test_add(self):
        for lhs, rhs, expected in list[tuple[Result, Result, Result]](
            [
                (
                    Result(),
                    Result(),
                    Result(),
                ),
                (
                    Result([chars.Char("a")]),
                    Result(),
                    Result([chars.Char("a")]),
                ),
                (
                    Result(),
                    Result([chars.Char("a")]),
                    Result([chars.Char("a")]),
                ),
                (
                    Result([chars.Char("a")]),
                    Result([chars.Char("b")]),
                    Result(
                        [
                            chars.Char("a"),
                            chars.Char("b"),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs + rhs, expected)

    def test_position(self):
        for result, expected in list[tuple[Result, Optional[chars.Position]]](
            [
                (
                    Result(),
                    None,
                ),
                (
                    Result([chars.Char("a")]),
                    chars.Position(),
                ),
                (
                    Result([chars.Char("a", chars.Position(1, 1))]),
                    chars.Position(1, 1),
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        result.position()
                else:
                    self.assertEqual(result.position(), expected)

    def test_value(self):
        for result, expected in list[tuple[Result, str]](
            [
                (
                    Result(),
                    "",
                ),
                (
                    Result([chars.Char("a")]),
                    "a",
                ),
                (
                    Result([chars.Char("a"), chars.Char("b")]),
                    "ab",
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(result.value(), expected)

    def test_load(self):
        for value, expected in list[tuple[str, Result]](
            [
                (
                    "",
                    Result(),
                ),
                (
                    "a",
                    Result([chars.Char("a")]),
                ),
                (
                    "ab",
                    Result([chars.Char("a"), chars.Char("b", chars.Position(0, 1))]),
                ),
            ]
        ):
            with self.subTest(value=value, expected=expected):
                self.assertEqual(Result.load(value), expected)
