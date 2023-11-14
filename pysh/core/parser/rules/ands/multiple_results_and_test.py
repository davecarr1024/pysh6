from unittest import TestCase
from pysh.core.parser import results, rules, states


class MultipleResultsAndTest(TestCase):
    def test_call(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                rules.Rule[states.State, int] | rules.Rule[states.State, str],
                rules.Rule[states.State, int] | rules.Rule[states.State, str],
                states.StateAndMultipleResults[states.State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).no().optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).no().multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).no().named(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, int](2).named(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).no(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).no().optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).no().multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).no().named(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, int](2).named(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, 2]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.MultipleResultsAnd[states.State, int, str]([lhs, rhs])(
                        states.State()
                    ),
                    expected,
                )
