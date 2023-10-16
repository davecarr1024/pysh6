from typing import Optional
from unittest import TestCase
from .. import chars
from ..regex import *


class RegexTest(TestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def test_apply(self):
        for regex, state, expected in list[
            tuple[Regex, chars.Stream | str, Optional[StateAndResult | str]]
        ](
            [
                (
                    Any(),
                    "a",
                    "a",
                ),
                (
                    Any(),
                    "",
                    None,
                ),
                (
                    Literal("a"),
                    "a",
                    "a",
                ),
                (
                    Literal("a"),
                    "",
                    None,
                ),
                (
                    Literal("a"),
                    "b",
                    None,
                ),
                (
                    And([Literal("a"), Literal("b")]),
                    "",
                    None,
                ),
                (
                    And([Literal("a"), Literal("b")]),
                    "a",
                    None,
                ),
                (
                    And([Literal("a"), Literal("b")]),
                    "b",
                    None,
                ),
                (
                    And([Literal("a"), Literal("b")]),
                    "ab",
                    "ab",
                ),
                (
                    Or([Literal("a"), Literal("b")]),
                    "",
                    None,
                ),
                (
                    Or([Literal("a"), Literal("b")]),
                    "c",
                    None,
                ),
                (
                    Or([Literal("a"), Literal("b")]),
                    "a",
                    "a",
                ),
                (
                    Or([Literal("a"), Literal("b")]),
                    "b",
                    "b",
                ),
                (
                    OneOrMore(Literal("a")),
                    "",
                    None,
                ),
                (
                    OneOrMore(Literal("a")),
                    "a",
                    "a",
                ),
                (
                    OneOrMore(Literal("a")),
                    "aa",
                    "aa",
                ),
                (
                    ZeroOrMore(Literal("a")),
                    "",
                    "",
                ),
                (
                    ZeroOrMore(Literal("a")),
                    "a",
                    "a",
                ),
                (
                    ZeroOrMore(Literal("a")),
                    "aa",
                    "aa",
                ),
                (
                    ZeroOrOne(Literal("a")),
                    "",
                    "",
                ),
                (
                    ZeroOrOne(Literal("a")),
                    "a",
                    "a",
                ),
                (
                    ZeroOrOne(Literal("a")),
                    "b",
                    (
                        chars.Stream.load("b"),
                        Result.load(""),
                    ),
                ),
                (
                    ZeroOrOne(Literal("a")),
                    "aa",
                    (
                        chars.Stream([chars.Char("a", chars.Position(0, 1))]),
                        Result.load("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(regex=regex, state=state, expected=expected):
                if isinstance(state, str):
                    state = chars.Stream.load(state)
                if expected is None:
                    with self.assertRaises(Error):
                        regex(state)
                else:
                    if isinstance(expected, str):
                        expected = (chars.Stream(), Result.load(expected))
                    actual = regex(state)
                    self.assertEqual(
                        actual,
                        expected,
                        f"actual {str(actual)} != expected {str(expected)}",
                    )
