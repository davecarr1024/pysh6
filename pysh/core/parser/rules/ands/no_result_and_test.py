from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules.ands import no_result_and
from pysh.core.parser.rules.literals import no_result_literal


class NoResultAndTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State[int], Optional[states.StateAndNoResult[int]]]
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
                                tokens.Token("a", "1"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State[int](
                        tokens.Stream(
                            [
                                tokens.Token("b", "1"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State[int](
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("b", "1"),
                            ]
                        )
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.State[int](
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("b", "1"),
                                tokens.Token("c", "1"),
                            ]
                        )
                    ),
                    states.StateAndNoResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "1"),
                                ]
                            )
                        ),
                        results.NoResult[int](),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = no_result_and.NoResultAnd[int](
                    [
                        no_result_literal.NoResultLiteral(
                            lexer.Rule.load("a"),
                        ),
                        no_result_literal.NoResultLiteral(
                            lexer.Rule.load("b"),
                        ),
                    ]
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
