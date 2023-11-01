from typing import Optional
from unittest import TestCase
from pysh.core import lexer, tokens

from pysh.core.parser import errors, results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import optional_result_literal


class OptionalResultLiteralTest(TestCase):
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
                                tokens.Token("int", "1"),
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
                                tokens.Token("int", "-1"),
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
                                tokens.Token("str", "a"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("int", "a"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("int", "1"),
                                tokens.Token("int", "2"),
                            ]
                        )
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "2"),
                                ]
                            )
                        ),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("int", "-1"),
                                tokens.Token("int", "2"),
                            ]
                        )
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "2"),
                                ]
                            )
                        ),
                        results.OptionalResult[int](),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert_int(token: tokens.Token) -> Optional[int]:
                    try:
                        value = int(token.value)
                        if value > 0:
                            return value
                        else:
                            return None
                    except Exception as error:
                        raise errors.Error(
                            msg=f"failed to convert {token} to int: {error}"
                        )

                rule = optional_result_literal.OptionalResultLiteral[int](
                    lexer.Rule.load("int", "a"),
                    convert_int,
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
                else:
                    self.assertEqual(
                        rule(state, scope.Scope()),
                        expected,
                    )
