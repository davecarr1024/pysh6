from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import token_value


class NoResultTypeConverterTest(TestCase):
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
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = (
                    token_value.TokenValue(lexer.Rule.load("a"))
                    .no()
                    .convert_type(lambda: 1)
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
                else:
                    self.assertEqual(rule(state, scope.Scope()), expected)
