from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class MultipleResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        self.assertEqual(
            (rules.Constant[State, str]("1") & rules.Constant[State, str]("2")).convert(
                lambda values: sum(map(int, values))
            )(State()),
            states.StateAndSingleResults[State, int](
                State(), results.SingleResults[int](3)
            ),
        )

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
                    rules.ands.MultipleResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).single(),
                    rules.ands.MultipleResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.ands.MultipleResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.ands.MultipleResultsAnd,
                ),
                (
                    rules.Constant[State, int](1).named(),
                    rules.ands.NamedResultsAnd,
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected_type=expected_type):
                lhs: rules.MultipleResultsRule[State, int] = rules.Constant[State, int](
                    1
                ).multiple()
                actual: rules.ands.And[State, int, rules.Rule[State, int]] = lhs & rhs
                self.assertSequenceEqual(list(actual), [lhs, rhs])
                self.assertIsInstance(actual, expected_type)
