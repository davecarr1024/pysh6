from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class OptionalResultsAndTest(TestCase):
    def test_ctor_fail(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs in list[
            tuple[
                Union[
                    rules.OptionalResultsRule[State, int],
                    rules.OptionalResultsRule[State, str],
                ],
                Union[
                    rules.OptionalResultsRule[State, int],
                    rules.OptionalResultsRule[State, str],
                ],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, int](2).optional(),
                ),
                (
                    rules.Constant[State, str]("a").optional(),
                    rules.Constant[State, str]("b").optional(),
                ),
                (
                    rules.Constant[State, str]("a").optional(),
                    rules.Constant[State, int](1).optional(),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs):
                with self.assertRaises(errors.Error):
                    rules.ands.OptionalResultsAnd[State, int, str]([lhs, rhs])

    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs, expected in list[
            tuple[
                rules.OptionalResultsRule[State, int]
                | rules.OptionalResultsRule[State, str],
                rules.NoResultsRule[State, int] | rules.NoResultsRule[State, str],
                states.StateAndOptionalResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no().optional(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().optional(),
                    rules.Constant[State, str]("b").no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().optional(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().optional(),
                    rules.Constant[State, str]("b").no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, str]("b").no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").optional(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").optional(),
                    rules.Constant[State, str]("b").no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.OptionalResultsAnd[State, int, str]([lhs, rhs])(State()),
                    expected,
                )
