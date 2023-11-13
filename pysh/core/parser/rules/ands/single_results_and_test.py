from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class SingleResultsAndTest(TestCase):
    def test_ctor_fail(self) -> None:
        for lhs, rhs in list[
            tuple[
                Union[
                    rules.SingleResultsRule[states.State, int],
                    rules.SingleResultsRule[states.State, str],
                ],
                Union[
                    rules.SingleResultsRule[states.State, int],
                    rules.SingleResultsRule[states.State, str],
                ],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1),
                    rules.Constant[states.State, int](2),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    rules.Constant[states.State, str]("b"),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    rules.Constant[states.State, int](1),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs):
                with self.assertRaises(errors.Error):
                    rules.ands.SingleResultsAnd[states.State, int, str]([lhs, rhs])

    def test_call(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                rules.SingleResultsRule[states.State, int]
                | rules.SingleResultsRule[states.State, str],
                rules.NoResultsRule[states.State, int]
                | rules.NoResultsRule[states.State, str],
                states.StateAndSingleResults[states.State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1),
                    rules.Constant[states.State, str]("b").no(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    rules.Constant[states.State, str]("b").no(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.SingleResultsAnd[states.State, int, str]([lhs, rhs])(
                        states.State()
                    ),
                    expected,
                )
