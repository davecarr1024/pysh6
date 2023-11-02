from unittest import TestCase
from pysh.core import lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import single_result_literal
from pysh.core.parser.rules.unary_rules import zero_or_more


class ZeroOrMoreTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State, states.StateAndMultipleResult[int]]
        ](
            [
                (
                    states.State(),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int](),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("i", "1"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("s", "a"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(
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
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("i", "1"),
                                tokens.Token("i", "2"),
                                tokens.Token("s", "a"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(
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
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("i"),
                        lambda token: int(token.value),
                    ).zero_or_more()(state, scope.Scope()),
                    expected,
                )
