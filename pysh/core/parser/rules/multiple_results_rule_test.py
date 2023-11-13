from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class MultipleResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        self.assertEqual(
            (
                rules.Constant[states.State, str]("1")
                & rules.Constant[states.State, str]("2")
            ).convert(lambda values: sum(map(int, values)))(states.State()),
            states.StateAndSingleResults[states.State, int](
                states.State(), results.SingleResults[int](3)
            ),
        )

    def test_and(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                rules.MultipleResultsRule[states.State, int],
                Union[
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, str],
                    rules.MultipleResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                ],
                states.StateAndResults[states.State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State()
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a").no().multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a").multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual((lhs & rhs)(states.State()), expected)
