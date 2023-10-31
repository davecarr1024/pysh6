from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules.literals import single_result_literal
from pysh.core.parser.rules.unary_rules import one_or_more


class OneOrMoreTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State[int], Optional[states.StateAndMultipleResult[int]]]
        ](
            [
                (
                    states.State[int](),
                    None,
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
                    None,
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
                rule = one_or_more.OneOrMore(
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("i"),
                        lambda token: int(token.value),
                    )
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
