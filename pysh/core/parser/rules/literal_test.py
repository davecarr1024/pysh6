from dataclasses import dataclass
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class LiteralTest(TestCase):
    def test_call(self):
        State = states.LexerState
        rule = State.literal(lexer.Rule.load("a"))
        with self.assertRaises(errors.Error):
            rule(State())
        self.assertEqual(
            rule(
                State(
                    states.LexerStateValue(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                            ]
                        )
                    )
                )
            ),
            states.StateAndSingleResults(
                State(),
                results.SingleResults[tokens.Token](tokens.Token("a", "1")),
            ),
        )
