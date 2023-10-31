from unittest import TestCase
from pysh.core import lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules.literals import single_result_literal
from pysh.core.parser.rules.unary_rules import zero_or_one


class ZeroOrOneTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State[int], states.StateAndOptionalResult[int]]
        ](
            [
                (
                    states.State[int](),
                    states.StateAndOptionalResult[int](
                        states.State[int](),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.State[int](
                        tokens.Stream(
                            [
                                tokens.Token("i", "1"),
                            ]
                        )
                    ),
                    states.StateAndOptionalResult[int](
                        states.State[int](),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.State[int](
                        tokens.Stream(
                            [
                                tokens.Token("s", "a"),
                            ]
                        )
                    ),
                    states.StateAndOptionalResult[int](
                        states.State[int](
                            tokens.Stream(
                                [
                                    tokens.Token("s", "a"),
                                ]
                            )
                        ),
                        results.OptionalResult[int](),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                self.assertEqual(
                    zero_or_one.ZeroOrOne(
                        single_result_literal.SingleResultLiteral[int](
                            lexer.Rule.load("i"),
                            lambda token: int(token.value),
                        )
                    )(state),
                    expected,
                )
