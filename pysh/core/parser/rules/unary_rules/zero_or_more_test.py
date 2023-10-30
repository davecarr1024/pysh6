from unittest import TestCase
from pysh.core import lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules.literals import single_result_literal
from pysh.core.parser.rules.unary_rules import zero_or_more


class ZeroOrMoreTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State[int], states.StateAndMultipleResult[int]]
        ](
            [
                (
                    states.State[int](),
                    states.StateAndMultipleResult[int](
                        states.State[int](),
                        results.MultipleResult[int](),
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
                    states.StateAndMultipleResult[int](
                        states.State[int](),
                        results.MultipleResult[int]([1]),
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
                    states.StateAndMultipleResult[int](
                        states.State[int](
                            tokens.Stream(
                                [
                                    tokens.Token("s", "a"),
                                ]
                            )
                        ),
                        results.MultipleResult[int]([]),
                    ),
                ),
                (
                    states.State[int](
                        tokens.Stream(
                            [
                                tokens.Token("i", "1"),
                                tokens.Token("i", "2"),
                                tokens.Token("s", "a"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State[int](
                            tokens.Stream(
                                [
                                    tokens.Token("s", "a"),
                                ]
                            )
                        ),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                self.assertEqual(
                    zero_or_more.ZeroOrMore(
                        single_result_literal.SingleResultLiteral[int](
                            lexer.Rule.load("i"),
                            lambda token: int(token.value),
                        )
                    )(state),
                    expected,
                )
