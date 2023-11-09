from dataclasses import dataclass, field
from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class RefTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True, kw_only=True)
        class State:
            lexer_result: lexer.Result = field(default_factory=lexer.Result)
            scope: rules.Scope["State", tokens.Token] = field(
                default_factory=rules.Scope["State", tokens.Token]
            )

            def __str__(self) -> str:
                return f"State(lexer_result={self.lexer_result}, scope={self.scope})"

            @staticmethod
            def lexer_result_setter() -> states.StateValueSetter["State", lexer.Result]:
                return states.StateValueSetter[State, lexer.Result].load(
                    lambda state: state.lexer_result,
                    lambda state, lexer_result: State(
                        lexer_result=lexer_result,
                        scope=state.scope,
                    ),
                )

            @staticmethod
            def literal(lexer_rule: lexer.Rule) -> rules.Literal["State"]:
                return rules.Literal[State](State.lexer_result_setter(), lexer_rule)

            @staticmethod
            def scope_getter() -> (
                states.StateValueGetter["State", rules.Scope["State", tokens.Token]]
            ):
                return states.StateValueGetter[
                    State, rules.Scope[State, tokens.Token]
                ].load(lambda state: state.scope)

            @staticmethod
            def ref(name: str) -> rules.Ref["State", tokens.Token]:
                return rules.Ref[State, tokens.Token](State.scope_getter(), name)

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
                        scope=rules.Scope[State, tokens.Token](
                            {
                                "s": State.literal(lexer.Rule.load("b")),
                            }
                        )
                    ),
                    None,
                ),
                (
                    State(
                        scope=rules.Scope[State, tokens.Token](
                            {
                                "r": State.literal(lexer.Rule.load("a")),
                            }
                        )
                    ),
                    None,
                ),
                (
                    State(
                        lexer_result=lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("b", "2"),
                                ]
                            )
                        ),
                        scope=rules.Scope[State, tokens.Token](
                            {
                                "r": State.literal(lexer.Rule.load("a")),
                            }
                        ),
                    ),
                    None,
                ),
                (
                    State(
                        lexer_result=lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("a", "1"),
                                ]
                            )
                        ),
                        scope=rules.Scope[State, tokens.Token](
                            {
                                "r": State.literal(lexer.Rule.load("a")),
                            }
                        ),
                    ),
                    states.StateAndSingleResults[State, tokens.Token](
                        State(
                            scope=rules.Scope[State, tokens.Token](
                                {
                                    "r": State.literal(lexer.Rule.load("a")),
                                }
                            ),
                        ),
                        results.SingleResults[tokens.Token](tokens.Token("a", "1")),
                    ),
                ),
                (
                    State(
                        lexer_result=lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("a", "1"),
                                    tokens.Token("b", "2"),
                                ]
                            )
                        ),
                        scope=rules.Scope[State, tokens.Token](
                            {
                                "r": State.literal(lexer.Rule.load("a")),
                            }
                        ),
                    ),
                    states.StateAndSingleResults[State, tokens.Token](
                        State(
                            lexer_result=lexer.Result(
                                tokens.Stream(
                                    [
                                        tokens.Token("b", "2"),
                                    ]
                                )
                            ),
                            scope=rules.Scope[State, tokens.Token](
                                {
                                    "r": State.literal(lexer.Rule.load("a")),
                                }
                            ),
                        ),
                        results.SingleResults[tokens.Token](tokens.Token("a", "1")),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = State.ref("r")
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    actual = rule(state)
                    self.assertEqual(
                        rule(state),
                        expected,
                        f"actual {actual} != expected {expected}",
                    )
