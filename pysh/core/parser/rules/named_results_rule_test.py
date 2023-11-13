from dataclasses import dataclass
from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors, lexer, tokens
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
        for lhs, rhs, state, expected in list[
            tuple[
                rules.NamedResultsRule[states.State, int],
                Union[
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                    str,
                ],
                states.State,
                Optional[states.StateAndResults[states.State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State()
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1, "": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().named(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a").no().named(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a"),
                    rules.Constant[states.State, str]("a").named("b"),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"a": 1, "b": "a"}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a")
                    & rules.Constant[states.State, int](2).named("b"),
                    "a",
                    states.State(),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1).named("a")
                    & rules.Constant[states.State, int](2).named("b"),
                    "a",
                    states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("a", "a"),
                                ]
                            )
                        )
                    ),
                    states.StateAndNamedResults[states.State, int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).named("a")
                    & rules.Constant[states.State, int](2).named("b"),
                    "a",
                    states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("b", "b"),
                                ]
                            )
                        )
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        (lhs & rhs)(state)
                else:
                    self.assertEqual((lhs & rhs)(state), expected)
