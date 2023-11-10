from dataclasses import dataclass
from typing import Type, Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class NamedResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        @dataclass(frozen=True)
        class Decl:
            name: str
            value: int

        self.assertEqual(
            (
                rules.Constant[State, str]("a").named("name")
                & rules.Constant[State, int](1).named("value")
            ).convert(Decl)(State()),
            states.StateAndSingleResults[State, Decl](
                State(), results.SingleResults[Decl](Decl("a", 1))
            ),
        )

    def test_and(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs, expected in list[
            tuple[
                rules.NamedResultsRule[State, int],
                Union[
                    rules.NoResultsRule[State, str],
                    rules.SingleResultsRule[State, str],
                    rules.OptionalResultsRule[State, str],
                    rules.NamedResultsRule[State, str],
                    rules.NamedResultsRule[State, str],
                ],
                states.StateAndResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, str]("a").no(),
                    states.StateAndNamedResults[State, int | str](State()),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, str]("a").no(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, str]("a"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": "a"}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, str]("a"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1, "": "a"}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, str]("a").no().optional(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, str]("a").optional(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": "a"}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, str]("a").no().named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, str]("a").named("b"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1, "b": "a"}),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual((lhs & rhs)(State()), expected)
