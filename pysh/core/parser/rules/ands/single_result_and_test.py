from typing import Optional, Sequence
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states

from pysh.core.parser.rules import no_result_rule, single_result_rule
from pysh.core.parser.rules.ands import single_result_and
from pysh.core.parser.rules.literals import no_result_literal, single_result_literal


class SingleResultAndTest(TestCase):
    def test_ctor_fail(self):
        for children in list[
            Sequence[
                no_result_rule.NoResultRule[int]
                | single_result_rule.SingleResultRule[int]
            ]
        ](
            [
                [],
                [
                    no_result_literal.NoResultLiteral[int](
                        lexer.Rule.load("a"),
                    )
                ],
                [
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("a"), lambda token: 1
                    ),
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("b"), lambda token: 2
                    ),
                ],
            ]
        ):
            with self.subTest(children=children):
                with self.assertRaises(errors.Error):
                    single_result_and.SingleResultAnd[int](children)

    def test_call(self):
        for state, expected in list[
            tuple[states.State[int], Optional[states.StateAndSingleResult[int]]]
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
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](2),
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
                    states.StateAndSingleResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.SingleResult[int](2),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = single_result_and.SingleResultAnd[int](
                    [
                        no_result_literal.NoResultLiteral[int](
                            lexer.Rule.load("a"),
                        ),
                        single_result_literal.SingleResultLiteral[int](
                            lexer.Rule.load("b"), lambda token: int(token.value)
                        ),
                    ]
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
