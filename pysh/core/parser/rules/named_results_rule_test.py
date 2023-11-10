from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import rules
from pysh.core.parser.rules.ands import (
    and_,
    named_results_and,
    optional_results_and,
)


class NamedResultsRuleTest(TestCase):
    def test_and(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for rhs, expected_type in list[
            tuple[
                Union[
                    rules.NoResultsRule[State, int],
                    rules.SingleResultsRule[State, int],
                    rules.OptionalResultsRule[State, int],
                    rules.MultipleResultsRule[State, int],
                    rules.NamedResultsRule[State, int],
                ],
                Type[and_.And[State, int, rules.Rule[State, int]]],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no(),
                    named_results_and.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).single(),
                    named_results_and.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    named_results_and.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    named_results_and.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).named(),
                    named_results_and.NamedResultsAnd,
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected_type=expected_type):
                lhs: rules.NamedResultsRule[State, int] = rules.Constant[State, int](
                    1
                ).named()
                actual: and_.And[State, int, rules.Rule[State, int]] = lhs & rhs
                self.assertSequenceEqual(list(actual), [lhs, rhs])
                self.assertIsInstance(actual, expected_type)
