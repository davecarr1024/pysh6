from dataclasses import dataclass, field
from typing import Callable, Optional
from unittest import TestCase
from pysh.core import errors, lexer, parser, regex, tokens


@dataclass(frozen=True)
class State:
    lexer_result: lexer.Result = field(default_factory=lexer.Result)

    @staticmethod
    def lexer_result_setter() -> parser.states.StateValueSetter["State", lexer.Result]:
        return parser.states.StateValueSetter[State, lexer.Result].load(
            lambda state: state.lexer_result,
            lambda _, lexer_result: State(lexer_result),
        )

    @staticmethod
    def literal(value: str | lexer.Rule) -> parser.rules.Literal["State"]:
        return parser.rules.Literal[State].load(
            State.lexer_result_setter(),
            value,
        )


class RuleTest(TestCase):
    def test_until(self) -> None:
        rule: parser.rules.MultipleResultsRule[State, int] = State.literal(
            r"\("
        ).no() & State.literal(lexer.Rule.load("int", r"\d+")).token_value().convert(
            int
        ).until(
            State.literal(r"\)").no()
        )
        for state, expected in list[
            tuple[
                State,
                Optional[parser.states.StateAndMultipleResults[State, int]],
            ]
        ](
            [
                (
                    State(),
                    None,
                ),
                (
                    State(
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
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                    tokens.Token(r"\)", ")"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[State, int](State()),
                ),
                (
                    State(
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
                    parser.states.StateAndMultipleResults[State, int](
                        State(),
                        parser.results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    State(
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
        rule: parser.rules.MultipleResultsRule[State, int] = (
            State.literal(lexer.Rule.load("int", r"\d+")).token_value().convert(int)
        ).until_empty(State.lexer_result_setter())
        for state, expected in list[
            tuple[
                State,
                Optional[parser.states.StateAndMultipleResults[State, int]],
            ]
        ](
            [
                (
                    State(),
                    parser.states.StateAndMultipleResults[State, int](State()),
                ),
                (
                    State(
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
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[State, int](
                        State(),
                        parser.results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                    tokens.Token("int", "2"),
                                ]
                            )
                        )
                    ),
                    parser.states.StateAndMultipleResults[State, int](
                        State(),
                        parser.results.MultipleResults[int]([1, 2]),
                    ),
                ),
                (
                    State(
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
