from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class NoResultConverterTest(TestCase):
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
                                tokens.Token("a", "a"),
                            ]
                        )
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](0)
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("b", "b"),
                            ]
                        )
                    ),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "a"),
                                tokens.Token("b", "b"),
                            ]
                        )
                    ),
                    states.StateAndSingleResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("b", "b"),
                                ]
                            )
                        ),
                        results.SingleResult[int](0),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = rules.literals.NoResultLiteral(lexer.Rule.load("a")).convert(
                    lambda: 0
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, rules.Scope())
                else:
                    self.assertEqual(rule(state, rules.Scope()), expected)
