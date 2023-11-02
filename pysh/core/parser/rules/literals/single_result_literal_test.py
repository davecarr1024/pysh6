from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import single_result_literal


class SingleResultLiteralTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[states.State, Optional[states.StateAndSingleResult[int]]]
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
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
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
                    states.StateAndSingleResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "2"),
                                ]
                            )
                        ),
                        results.SingleResult[int](1),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert_int(token: tokens.Token) -> int:
                    try:
                        return int(token.value)
                    except Exception as error:
                        raise errors.Error(msg=f"{error}")

                rule = single_result_literal.SingleResultLiteral[int](
                    lexer.Rule.load("int"),
                    convert_int,
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
                        assert 0
                else:
                    self.assertEqual(
                        rule(state, scope.Scope()),
                        expected,
                    )
