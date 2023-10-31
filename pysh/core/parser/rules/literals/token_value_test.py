from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states

from pysh.core.parser.rules.literals import token_value


class TokenValueTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State[str],
                Optional[states.StateAndSingleResult[str]],
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
                    states.StateAndSingleResult[str](
                        states.State(),
                        results.SingleResult[str]("1"),
                    ),
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
                    states.StateAndSingleResult[str](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("b", "2"),
                                ]
                            )
                        ),
                        results.SingleResult[str]("1"),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = token_value.TokenValue(lexer.Rule.load("a"))
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
