from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens

from pysh.core.parser import results, states
from pysh.core.parser.rules.converters import single_result_converter
from pysh.core.parser.rules.literals import token_value


class SingleResultConverterTest(TestCase):
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
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(result: str) -> int:
                    return int(result)

                rule = (
                    token_value.TokenValue(lexer.Rule.load("a"))
                    .single()
                    .convert(convert)
                )
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
