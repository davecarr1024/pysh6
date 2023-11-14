from dataclasses import dataclass, field
from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class LiteralTest(TestCase):
    def test_call(self) -> None:
        for state, expected in list[
            tuple[
                states.State,
                Optional[states.StateAndSingleResults[states.State, tokens.Token]],
            ]
        ](
            [
                (
                    states.State(),
                    None,
                ),
                (
                    states.State(
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
                    states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("r", "a"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[states.State, tokens.Token](
                        states.State(),
                        results.SingleResults[tokens.Token](tokens.Token("r", "a")),
                    ),
                ),
                (
                    states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("r", "a"),
                                    tokens.Token("s", "b"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[states.State, tokens.Token](
                        states.State(
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
            rule = rules.Literal[states.State](lexer.Rule.load("r", "a"))
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
