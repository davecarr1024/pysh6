from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class SingleResultsAndTest(TestCase):
    def test_ctor_fail(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs in list[
            tuple[
                Union[
                    rules.SingleResultsRule[State, int],
                    rules.SingleResultsRule[State, str],
                ],
                Union[
                    rules.SingleResultsRule[State, int],
                    rules.SingleResultsRule[State, str],
                ],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1),
                    rules.Constant[State, int](2),
                ),
                (
                    rules.Constant[State, str]("a"),
                    rules.Constant[State, str]("b"),
                ),
                (
                    rules.Constant[State, str]("a"),
                    rules.Constant[State, int](1),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs):
                with self.assertRaises(errors.Error):
                    rules.ands.SingleResultsAnd[State, int, str]([lhs, rhs])

    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs, expected in list[
            tuple[
                rules.SingleResultsRule[State, int]
                | rules.SingleResultsRule[State, str],
                rules.NoResultsRule[State, int] | rules.NoResultsRule[State, str],
                states.StateAndSingleResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1),
                    rules.Constant[State, int](2).no(),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, int](1),
                    rules.Constant[State, str]("b").no(),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, str]("a"),
                    rules.Constant[State, int](2).no(),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[State, str]("a"),
                    rules.Constant[State, str]("b").no(),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.SingleResultsAnd[State, int, str]([lhs, rhs])(State()),
                    expected,
                )
