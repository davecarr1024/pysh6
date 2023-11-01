from unittest import TestCase

from typing import Optional
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.ands import multiple_result_and
from pysh.core.parser.rules.literals import no_result_literal, single_result_literal


class MultipleResultAnd(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State, Optional[states.StateAndMultipleResult[int]]]
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
                                tokens.Token("a", "1"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("b", "2"),
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
                                tokens.Token("b", "2"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("b", "2"),
                                tokens.Token("c", "3"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(token: tokens.Token) -> int:
                    try:
                        return int(token.value)
                    except Exception as error:
                        raise errors.Error(
                            msg=f"failed to convert {token} to int: {error}"
                        )

                rule = multiple_result_and.MultipleResultAnd[int](
                    [
                        single_result_literal.SingleResultLiteral[int](
                            lexer.Rule.load("a"),
                            convert,
                        ),
                        single_result_literal.SingleResultLiteral[int](
                            lexer.Rule.load("b"),
                            convert,
                        ),
                    ]
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
                else:
                    self.assertEqual(rule(state, scope.Scope()), expected)
