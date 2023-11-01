from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import single_result_literal
from pysh.core.parser.rules.ors import named_result_or


class NamedResultOrTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State,
                Optional[states.StateAndNamedResult[int]],
            ]
        ](
            [
                (
                    states.State(),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("c", "3"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                            ]
                        )
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("b", "2"),
                            ]
                        )
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"b": 2}),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("c", "3"),
                            ]
                        )
                    ),
                    states.StateAndNamedResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.NamedResult[int]({"a": 1}),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(token: tokens.Token) -> int:
                    return int(token.value)

                rule = single_result_literal.SingleResultLiteral(
                    lexer.Rule.load("a"), convert
                ).named("a") | single_result_literal.SingleResultLiteral(
                    lexer.Rule.load("b"), convert
                ).named(
                    "b"
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
