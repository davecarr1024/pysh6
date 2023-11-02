from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import single_result_literal


class NamedResultTypeConverterTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State,
                Optional[states.StateAndSingleResult[int]],
            ]
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
                        results.SingleResult[int](3),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(*, a: int, b: int, **_) -> int:
                    return a + b

                rule = (
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("a"), lambda token: int(token.value)
                    ).named("a")
                    & single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("b"), lambda token: int(token.value)
                    ).named("b")
                ).convert_type(convert)
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
                else:
                    actual = rule(state, scope.Scope())
                    self.assertEqual(actual, expected, msg=f"{actual} != {expected}")
