from dataclasses import dataclass, field
from typing import Callable, Optional
from unittest import TestCase
from pysh.core import errors, lexer, parser, regex, tokens


class RuleTest(TestCase):
    def test_until(self) -> None:
        rule: parser.rules.MultipleResultsRule[
            parser.states.State, int
        ] = parser.rules.Literal[parser.states.State].load(
            r"\("
        ).no() & parser.rules.Literal[
            parser.states.State
        ](
            lexer.Rule.load("int", r"\d+")
        ).token_value().convert(
            int
        ).until(
            parser.rules.Literal[parser.states.State].load(r"\)").no()
        )
        for state, expected in list[
            tuple[
                parser.states.State,
                Optional[
                    parser.states.StateAndMultipleResults[parser.states.State, int]
                ],
            ]
        ](
            [
                (
                    parser.states.State(),
                    None,
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                ]
                            )
                        )
                    ),
                    None,
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                    tokens.Token(r"\)", ")"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[parser.states.State, int](
                        parser.states.State()
                    ),
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                    tokens.Token("int", "1"),
                                    tokens.Token(r"\)", ")"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[parser.states.State, int](
                        parser.states.State(),
                        parser.results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                    tokens.Token("int", "1"),
                                ]
                            )
                        )
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)

    def test_until_empty(self) -> None:
        rule: parser.rules.MultipleResultsRule[parser.states.State, int] = (
            parser.rules.Literal[parser.states.State](lexer.Rule.load("int", r"\d+"))
            .token_value()
            .convert(int)
        ).until_empty()
        for state, expected in list[
            tuple[
                parser.states.State,
                Optional[
                    parser.states.StateAndMultipleResults[parser.states.State, int]
                ],
            ]
        ](
            [
                (
                    parser.states.State(),
                    parser.states.StateAndMultipleResults[parser.states.State, int](
                        parser.states.State()
                    ),
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("str", '"a"'),
                                ]
                            )
                        )
                    ),
                    None,
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[parser.states.State, int](
                        parser.states.State(),
                        parser.results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                    tokens.Token("int", "2"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[parser.states.State, int](
                        parser.states.State(),
                        parser.results.MultipleResults[int]([1, 2]),
                    ),
                ),
                (
                    parser.states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                    tokens.Token("str", '"a"'),
                                ]
                            )
                        )
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
