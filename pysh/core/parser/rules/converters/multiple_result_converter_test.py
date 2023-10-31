from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules.literals import single_result_literal


class MultipleResultConverterTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State[int],
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
                        states.State[int](),
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
                        states.State[int](),
                        results.SingleResult[int](2),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = (
                    single_result_literal.SingleResultLiteral[int](
                        lexer.Rule.load("a"), lambda token: int(token.value)
                    )
                    .one_or_more()
                    .convert(lambda results_: results.SingleResult[int](sum(results_)))
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
