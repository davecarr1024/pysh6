from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class NoResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        self.assertEqual(
            rules.Constant[State, str]("1").convert(int)(State()),
            states.StateAndSingleResults[State, int](
                State(), results.SingleResults[int](1)
            ),
        )

    def test_and(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for rhs, expected in list[
            tuple[
                Union[
                    rules.NoResultsRule[State, str],
                    rules.SingleResultsRule[State, str],
                    rules.OptionalResultsRule[State, str],
                    rules.MultipleResultsRule[State, str],
                    rules.NamedResultsRule[State, str],
                ],
                states.StateAndResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, str]("a").no(),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, str]("a"),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": 1}),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").named("v"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"v": "a", "": 1}),
                    ),
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected=expected):
                lhs: rules.SingleResultsRule[State, int] = rules.Constant[State, int](1)
                self.assertEqual((lhs & rhs)(State()), expected)
