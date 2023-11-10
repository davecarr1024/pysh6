from dataclasses import dataclass
from typing import Optional, Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class NoResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        def convert(value: Optional[str]) -> int:
            return int(value) if value is not None else -1

        self.assertEqual(
            rules.Constant[State, str]("1").optional().convert(convert)(State()),
            states.StateAndSingleResults[State, int](
                State(), results.SingleResults[int](1)
            ),
        )

    def test_and(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs, expected in list[
            tuple[
                rules.OptionalResultsRule[State, int],
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
                    rules.Constant[State, int](1).no().optional(),
                    rules.Constant[State, str]("a").no(),
                    states.StateAndOptionalResults[State, int | str](State()),
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, str]("a").no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().optional(),
                    rules.Constant[State, str]("a"),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, str]("a"),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().optional(),
                    rules.Constant[State, str]("a").no().optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().optional(),
                    rules.Constant[State, str]("a").optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, str]("a").no().optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional(),
                    rules.Constant[State, str]("a").optional(),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual((lhs & rhs)(State()), expected)
