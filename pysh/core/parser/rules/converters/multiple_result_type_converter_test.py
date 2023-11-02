from typing import Optional, Sequence
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import single_result_literal


class MultipleResultTypeConverterTest(TestCase):
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
                                tokens.Token("a", "1"),
                                tokens.Token("a", "1"),
                            ]
                        )
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](2),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(results: Sequence[int]) -> int:
                    return sum(results)

                rule = (
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("a"), lambda token: int(token.value)
                    )
                    .one_or_more()
                    .convert_type(convert)
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
                else:
                    self.assertEqual(rule(state, scope.Scope()), expected)