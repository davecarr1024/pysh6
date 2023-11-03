from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class SingleResultConverterTest(TestCase):
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
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](2),
                    ),
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
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("b", "2"),
                                ]
                            )
                        ),
                        results.SingleResult[int](2),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = rules.literals.SingleResultLiteral(
                    lexer.Rule.load("a"), lambda token: int(token.value)
                ).convert(lambda result: result * 2)
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, rules.Scope())
                else:
                    self.assertEqual(rule(state, rules.Scope()), expected)
