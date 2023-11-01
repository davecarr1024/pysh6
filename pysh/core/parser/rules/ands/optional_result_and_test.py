from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.ands import optional_result_and
from pysh.core.parser.rules.literals import no_result_literal, optional_result_literal


class OptionalResultAndTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State, Optional[states.StateAndOptionalResult[int]]]
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
                                tokens.Token("b", "-2"),
                            ]
                        )
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
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
                    states.StateAndOptionalResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.OptionalResult[int](2),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("b", "-2"),
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
                        results.OptionalResult[int](),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(token: tokens.Token) -> Optional[int]:
                    try:
                        value = int(token.value)
                        if value > 0:
                            return value
                        else:
                            return None
                    except Exception as error:
                        raise errors.Error(msg=f"failed to convert int: {error}")

                rule = optional_result_and.OptionalResultAnd[int](
                    [
                        no_result_literal.NoResultLiteral[int](
                            lexer.Rule.load("a"),
                        ),
                        optional_result_literal.OptionalResultLiteral[int](
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
