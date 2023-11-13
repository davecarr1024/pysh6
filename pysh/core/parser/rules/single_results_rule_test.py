from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors, lexer, tokens
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
        for rhs, state, expected in list[
            tuple[
                Union[
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, str],
                    rules.MultipleResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                    lexer.Rule,
                    str,
                ],
                states.State,
                Optional[states.StateAndResults[states.State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().multiple(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").multiple(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().named(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"": 1}),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").named("v"),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"v": "a", "": 1}),
                    ),
                ),
                (
                    "a",
                    states.State(),
                    None,
                ),
                (
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
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
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
                (
                    lexer.Rule.load("a"),
                    states.State(),
                    None,
                ),
                (
                    lexer.Rule.load("a"),
                    states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("a", "a"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    lexer.Rule.load("a"),
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
            with self.subTest(rhs=rhs, state=state, expected=expected):
                lhs: rules.SingleResultsRule[states.State, int] = rules.Constant[
                    states.State, int
                ](1)
                if expected is None:
                    with self.assertRaises(errors.Error):
                        (lhs & rhs)(state)
                else:
                    self.assertEqual((lhs & rhs)(state), expected)

    def test_rand(self) -> None:
        for lhs, state, expected in list[
            tuple[
                Union[
                    str,
                    lexer.Rule,
                ],
                states.State,
                Optional[states.StateAndResults[states.State, int]],
            ]
        ](
            [
                (
                    "a",
                    states.State(),
                    None,
                ),
                (
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
                    states.StateAndSingleResults[states.State, int](
                        states.State(),
                        results.SingleResults[int](1),
                    ),
                ),
                (
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
                (
                    lexer.Rule.load("a"),
                    states.State(),
                    None,
                ),
                (
                    lexer.Rule.load("a"),
                    states.State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("a", "a"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[states.State, int](
                        states.State(),
                        results.SingleResults[int](1),
                    ),
                ),
                (
                    lexer.Rule.load("a"),
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
            with self.subTest(lhs=lhs, state=state, expected=expected):
                rhs: rules.SingleResultsRule[states.State, int] = rules.Constant[
                    states.State, int
                ](1).single()
                if expected is None:
                    with self.assertRaises(errors.Error):
                        (lhs & rhs)(state)
                else:
                    self.assertEqual((lhs & rhs)(state), expected)
