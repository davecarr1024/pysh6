from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class OptionalResultsAndTest(TestCase):
    def test_ctor_fail(self) -> None:
        for lhs, rhs in list[
            tuple[
                Union[
                    rules.OptionalResultsRule[states.State, int],
                    rules.OptionalResultsRule[states.State, str],
                ],
                Union[
                    rules.OptionalResultsRule[states.State, int],
                    rules.OptionalResultsRule[states.State, str],
                ],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, int](2).optional(),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    rules.Constant[states.State, str]("b").optional(),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    rules.Constant[states.State, int](1).optional(),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs):
                with self.assertRaises(errors.Error):
                    rules.ands.OptionalResultsAnd[states.State, int, str]([lhs, rhs])

    def test_call(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                rules.OptionalResultsRule[states.State, int]
                | rules.OptionalResultsRule[states.State, str],
                rules.NoResultsRule[states.State, int]
                | rules.NoResultsRule[states.State, str],
                states.StateAndOptionalResults[states.State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("b").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().optional(),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().optional(),
                    rules.Constant[states.State, str]("b").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("b").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    rules.Constant[states.State, str]("b").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.OptionalResultsAnd[states.State, int, str]([lhs, rhs])(
                        states.State()
                    ),
                    expected,
                )
