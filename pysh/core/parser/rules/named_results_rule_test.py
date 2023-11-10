from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


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
                Type[rules.ands.And[State, int, rules.Rule[State, int]]],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no(),
                    rules.ands.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).single(),
                    rules.ands.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.ands.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.ands.NamedResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).named(),
                    rules.ands.NamedResultsAnd,
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected_type=expected_type):
                lhs: rules.NamedResultsRule[State, int] = rules.Constant[State, int](
                    1
                ).named()
                actual: rules.ands.And[State, int, rules.Rule[State, int]] = lhs & rhs
                self.assertSequenceEqual(list(actual), [lhs, rhs])
                self.assertIsInstance(actual, expected_type)

    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        def convert(*, a: int, b: int) -> int:
            return a * 10 + b

        self.assertEqual(
            (
                rules.Constant[State, int](1).named("a")
                & rules.Constant[State, int](2).named("b")
            ).convert(convert)(State()),
            states.StateAndSingleResults[State, int](
                State(), results.SingleResults[int](12)
            ),
        )
