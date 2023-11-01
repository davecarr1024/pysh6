from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, rules, states


class ReferenceTest(TestCase):
    def test_call(self):
        for state, scope, expected in list[
            tuple[
                states.State,
                rules.Scope[int],
                Optional[states.StateAndSingleResult[int]],
            ]
        ](
            [
                (
                    states.State(),
                    rules.Scope(),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("i", "1"),
                            ]
                        ),
                    ),
                    rules.Scope(),
                    None,
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("i", "1"),
                            ]
                        ),
                    ),
                    rules.Scope[int](
                        {
                            "a": rules.literals.SingleResultLiteral[int](
                                lexer.Rule.load("i"),
                                lambda token: int(token.value),
                            ),
                        }
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, scope=scope, expected=expected):
                rule = rules.Reference("a")
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope)
                else:
                    self.assertEqual(rule(state, scope), expected)
