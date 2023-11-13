from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class NoResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        self.assertEqual(
            rules.Constant[states.State, str]("1").convert(int)(states.State()),
            states.StateAndSingleResults[states.State, int](
                states.State(), results.SingleResults[int](1)
            ),
        )

    def test_and(self) -> None:
        for rhs, expected in list[
            tuple[
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
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").multiple(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().named(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"": 1}),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").named("v"),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"v": "a", "": 1}),
                    ),
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected=expected):
                lhs: rules.SingleResultsRule[states.State, int] = rules.Constant[
                    states.State, int
                ](1)
                self.assertEqual((lhs & rhs)(states.State()), expected)
