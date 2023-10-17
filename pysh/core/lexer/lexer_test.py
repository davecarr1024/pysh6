from typing import Mapping, Optional, Sequence
from unittest import TestCase
from .. import chars, regex, tokens
from . import lex_error, lexer, rule


class LexerTest(TestCase):
    def test_load(self):
        for regexes, expected in list[
            tuple[Mapping[str, str | regex.Regex], lexer.Lexer]
        ](
            [
                (
                    {},
                    lexer.Lexer(),
                ),
                (
                    {
                        "a": "a",
                    },
                    lexer.Lexer([rule.Rule.load("a")]),
                ),
                (
                    {
                        "r": "a",
                    },
                    lexer.Lexer([rule.Rule.load("r", "a")]),
                ),
                (
                    {
                        "r": regex.Literal("a"),
                    },
                    lexer.Lexer([rule.Rule.load("r", "a")]),
                ),
                (
                    {
                        "r": "a",
                        "s": "b",
                    },
                    lexer.Lexer(
                        [
                            rule.Rule.load("r", "a"),
                            rule.Rule.load("s", "b"),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(regexes=regexes, expected=expected):
                self.assertEqual(lexer.Lexer.load(**regexes), expected)

    def test_literal(self):
        for values, expected in list[tuple[Sequence[str], lexer.Lexer]](
            [
                (
                    [],
                    lexer.Lexer(),
                ),
                (
                    ["a"],
                    lexer.Lexer([rule.Rule.load("a")]),
                ),
                (
                    ["a", "b"],
                    lexer.Lexer(
                        [
                            rule.Rule.load("a"),
                            rule.Rule.load("b"),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(values=values, expected=expected):
                self.assertEqual(lexer.Lexer.literal(*values), expected)

    def test_or(self):
        for lhs, rhs, expected in list[tuple[lexer.Lexer, lexer.Lexer, lexer.Lexer]](
            [
                (
                    lexer.Lexer(),
                    lexer.Lexer(),
                    lexer.Lexer(),
                ),
                (
                    lexer.Lexer.literal("a"),
                    lexer.Lexer(),
                    lexer.Lexer.literal("a"),
                ),
                (
                    lexer.Lexer(),
                    lexer.Lexer.literal("a"),
                    lexer.Lexer.literal("a"),
                ),
                (
                    lexer.Lexer.literal("a"),
                    lexer.Lexer.literal("b"),
                    lexer.Lexer.literal("a", "b"),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)

    def test_call(self):
        for lexer_, state, expected in list[
            tuple[lexer.Lexer, str | chars.Stream, Optional[tokens.Stream]]
        ](
            [
                (
                    lexer.Lexer(),
                    "",
                    tokens.Stream(),
                ),
                (
                    lexer.Lexer.load(r="a"),
                    "a",
                    tokens.Stream([tokens.Token("r", "a")]),
                ),
                (
                    lexer.Lexer.load(r="a"),
                    "b",
                    None,
                ),
                (
                    lexer.Lexer.load(r="a"),
                    "aa",
                    tokens.Stream(
                        [
                            tokens.Token("r", "a"),
                            tokens.Token("r", "a", chars.Position(0, 1)),
                        ]
                    ),
                ),
                (
                    lexer.Lexer.load(r="a"),
                    "ab",
                    None,
                ),
                (
                    lexer.Lexer.load(r="a", s="b"),
                    "ab",
                    tokens.Stream(
                        [
                            tokens.Token("r", "a"),
                            tokens.Token("s", "b", chars.Position(0, 1)),
                        ]
                    ),
                ),
                (
                    lexer.Lexer.load(r="a", s="b"),
                    "abc",
                    None,
                ),
            ]
        ):
            with self.subTest(lexer_=lexer_, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(lex_error.LexError):
                        lexer_(state)
                else:
                    self.assertEqual(lexer_(state), expected)
