from dataclasses import dataclass, field
from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class LiteralTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            lexer_result: lexer.Result = field(default_factory=lexer.Result)

            @staticmethod
            def lexer_result_setter() -> states.StateValueSetter["State", lexer.Result]:
                return states.StateValueSetter[State, lexer.Result].load(
                    lambda state: state.lexer_result,
                    lambda _, lexer_result: State(lexer_result),
                )

            @staticmethod
            def literal(lexer_rule: lexer.Rule) -> rules.Literal["State"]:
                return rules.Literal[State](State.lexer_result_setter(), lexer_rule)

        for state, expected in list[
            tuple[
                State,
                Optional[states.StateAndSingleResults[State, tokens.Token]],
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
                                    tokens.Token("s", "b"),
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
                                    tokens.Token("r", "a"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, tokens.Token](
                        State(),
                        results.SingleResults[tokens.Token](tokens.Token("r", "a")),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("r", "a"),
                                    tokens.Token("s", "b"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, tokens.Token](
                        State(
                            lexer.Result(
                                tokens.Stream(
                                    [
                                        tokens.Token("s", "b"),
                                    ]
                                )
                            )
                        ),
                        results.SingleResults[tokens.Token](tokens.Token("r", "a")),
                    ),
                ),
            ]
        ):
            rule = State.literal(lexer.Rule.load("r", "a"))
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
