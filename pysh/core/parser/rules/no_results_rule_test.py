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
            rules.Constant[State, str]("1").no().convert(lambda: 1)(State()),
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
                    states.StateAndNoResults[State, int | str](State()),
                ),
                (
                    rules.Constant[State, str]("a"),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().optional(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").optional(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").multiple(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").no().named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, str]("a").named("v"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"v": "a"}),
                    ),
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected=expected):
                lhs: rules.NoResultsRule[State, int] = rules.Constant[State, int](
                    1
                ).no()
                self.assertEqual((lhs & rhs)(State()), expected)
