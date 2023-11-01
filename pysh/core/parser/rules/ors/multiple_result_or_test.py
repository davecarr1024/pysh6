from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import single_result_literal
from pysh.core.parser.rules.ors import multiple_result_or


class MultipleResultOrTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State,
                Optional[states.StateAndMultipleResult[int]],
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
                                tokens.Token("c", "3"),
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
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
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
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([2]),
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
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("b", "2"),
                                tokens.Token("c", "3"),
                            ]
                        )
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):

                def convert(token: tokens.Token) -> int:
                    return int(token.value)

                rule = (
                    single_result_literal.SingleResultLiteral(
                        lexer.Rule.load("a"), convert
                    ).multiple()
                    | single_result_literal.SingleResultLiteral(
                        lexer.Rule.load("b"), convert
                    ).multiple()
                ).one_or_more()
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
