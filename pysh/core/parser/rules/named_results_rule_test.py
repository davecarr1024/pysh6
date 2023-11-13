from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core.parser import results, rules, states


class NamedResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class Decl:
            name: str
            value: int

        self.assertEqual(
            (
                rules.Constant[states.State, str]("a").named("name")
                & rules.Constant[states.State, int](1).named("value")
            ).convert(Decl)(states.State()),
            states.StateAndSingleResults[states.State, Decl](
                states.State(), results.SingleResults[Decl](Decl("a", 1))
            ),
        )

    def test_and(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                rules.NamedResultsRule[states.State, int],
                Union[
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                ],
                states.StateAndResults[states.State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State()
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1, "": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a").no().named(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a").named("b"),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1, "b": "a"}),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual((lhs & rhs)(states.State()), expected)
