from typing import Optional
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import scope
from pysh.core.parser.rules.literals import no_result_literal
from pysh.core.parser.rules.ors import no_result_or


class NoResultOrTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                states.State,
                Optional[states.StateAndNoResult[int]],
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
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
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
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.State(
                        tokens.Stream(
                            [
                                tokens.Token("a", "1"),
                                tokens.Token("c", "3"),
                            ]
                        )
                    ),
                    states.StateAndNoResult[int](
                        states.State(
                            tokens.Stream(
                                [
                                    tokens.Token("c", "3"),
                                ]
                            )
                        ),
                        results.NoResult[int](),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = no_result_literal.NoResultLiteral(
                    lexer.Rule.load("a")
                ) | no_result_literal.NoResultLiteral(lexer.Rule.load("b"))
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state, scope.Scope())
