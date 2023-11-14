from typing import Mapping, Optional, Sequence
from unittest import TestCase
from pysh.core import chars, errors, lexer, regex, tokens


class LexerTest(TestCase):
    def test_literal(self):
        for values, expected in list[
            tuple[
                Sequence[str],
                lexer.Lexer,
            ]
        ](
            [
                (
                    [],
                    lexer.Lexer(),
                ),
                (
                    ["a"],
                    lexer.Lexer(
                        [
                            lexer.Rule("a", regex.Literal("a")),
                        ]
                    ),
                ),
                (
                    ["a", "b"],
                    lexer.Lexer(
                        [
                            lexer.Rule("a", regex.Literal("a")),
                            lexer.Rule("b", regex.Literal("b")),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(values=values, expected=expected):
                self.assertEqual(lexer.Lexer.literal(*values), expected)

    def test_load(self):
        for values, expected in list[
            tuple[
                Mapping[str, str | regex.Regex],
                lexer.Lexer,
            ]
        ](
            [
                (
                    {},
                    lexer.Lexer(),
                ),
                (
                    {"r": "a"},
                    lexer.Lexer(
                        [
                            lexer.Rule("r", regex.Literal("a")),
                        ]
                    ),
                ),
                (
                    {"r": regex.Literal("a")},
                    lexer.Lexer(
                        [
                            lexer.Rule("r", regex.Literal("a")),
                        ]
                    ),
                ),
                (
                    {
                        "r": regex.Literal("a"),
                        "s": "b",
                    },
                    lexer.Lexer(
                        [
                            lexer.Rule("r", regex.Literal("a")),
                            lexer.Rule("s", regex.Literal("b")),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(values=values, expected=expected):
                self.assertEqual(lexer.Lexer.load(**values), expected)

    def test_call(self):
        for state, expected in list[
            tuple[
                lexer.State,
                Optional[lexer.Result],
            ]
        ](
            [
                (
                    lexer.State(),
                    lexer.Result(),
                ),
                (
                    lexer.State.load("a"),
                    lexer.Result(
                        tokens.Stream(
                            [
                                tokens.Token("r", "a"),
                            ]
                        )
                    ),
                ),
                (
                    lexer.State.load("b"),
                    lexer.Result(
                        tokens.Stream(
                            [
                                tokens.Token("s", "b"),
                            ]
                        )
                    ),
                ),
                (
                    lexer.State.load("ab"),
                    lexer.Result(
                        tokens.Stream(
                            [
                                tokens.Token("r", "a"),
                                tokens.Token("s", "b", chars.Position(0, 1)),
                            ]
                        )
                    ),
                ),
                (
                    lexer.State.load("\na b\t"),
                    lexer.Result(
                        tokens.Stream(
                            [
                                tokens.Token("r", "a", chars.Position(1, 0)),
                                tokens.Token("s", "b", chars.Position(1, 2)),
                            ]
                        )
                    ),
                ),
                (
                    lexer.State.load("c"),
                    None,
                ),
                (
                    lexer.State.load("abc"),
                    None,
                ),
            ]
        ):
            lexer_ = lexer.Lexer.load(r="a", s="b") | lexer.Lexer(
                [lexer.Rule.load("~ws", r"\s+")]
            )
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        lexer_(state)
                else:
                    self.assertEqual(lexer_(state), expected)
