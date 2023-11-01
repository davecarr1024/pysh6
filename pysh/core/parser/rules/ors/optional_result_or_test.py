from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import optional_result_literal
from pysh.core.parser.rules.ors import optional_result_or


class OptionalResultOrTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State,
                Optional[states.StateAndOptionalResult[int]],
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
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
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
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](2),
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
                    states.StateAndOptionalResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.OptionalResult[int](1),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(token: tokens.Token) -> int:
                    return int(token.value)

                rule = optional_result_literal.OptionalResultLiteral(
                    lexer.Rule.load("a"), convert
                ) | optional_result_literal.OptionalResultLiteral(
                    lexer.Rule.load("b"), convert
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
