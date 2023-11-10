from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class MultipleResultsAndTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs, expected in list[
            tuple[
                rules.Rule[State, int] | rules.Rule[State, str],
                rules.Rule[State, int] | rules.Rule[State, str],
                states.StateAndMultipleResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).no().optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).no().multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).no().named(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().multiple(),
                    rules.Constant[State, int](2).named(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).no().optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).no().multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).no().named(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).multiple(),
                    rules.Constant[State, int](2).named(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.MultipleResultsAnd[State, int, str]([lhs, rhs])(State()),
                    expected,
                )
