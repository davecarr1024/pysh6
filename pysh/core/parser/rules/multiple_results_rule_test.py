from dataclasses import dataclass
from typing import Optional, Sequence, Type, Union
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class MultipleResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        def convert(values: Sequence[str]) -> int:
            s: int = 0
            for value in values:
                s += int(value)
            return s

        self.assertEqual(
            (
                rules.Constant[states.State, str]("1")
                & rules.Constant[states.State, str]("2")
            ).convert(convert)(states.State()),
            states.StateAndSingleResults[states.State, int](
                states.State(), results.SingleResults[int](3)
            ),
        )

    def test_and(self) -> None:
        for lhs, rhs, state, expected in list[
            tuple[
                rules.MultipleResultsRule[states.State, int],
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
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State()
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().multiple(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a").no().multiple(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).multiple(),
                    rules.Constant[states.State, str]("a").multiple(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1)
                    & rules.Constant[states.State, int](2),
                    "a",
                    states.State(),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1)
                    & rules.Constant[states.State, int](2),
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
                    states.StateAndMultipleResults[states.State, int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1)
                    & rules.Constant[states.State, int](2),
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
                    rules.Constant[states.State, int](1)
                    & rules.Constant[states.State, int](2),
                    lexer.Rule.load("a"),
                    states.State(),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1)
                    & rules.Constant[states.State, int](2),
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
                    states.StateAndMultipleResults[states.State, int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1)
                    & rules.Constant[states.State, int](2),
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
            with self.subTest(lhs=lhs, rhs=rhs, state=state, expected=expected):
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
                    states.StateAndMultipleResults[states.State, int](
                        states.State(),
                        results.MultipleResults[int]([1]),
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
                    states.StateAndMultipleResults[states.State, int](
                        states.State(),
                        results.MultipleResults[int]([1]),
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
                rhs: rules.MultipleResultsRule[states.State, int] = rules.Constant[
                    states.State, int
                ](1).multiple()
                if expected is None:
                    with self.assertRaises(errors.Error):
                        (lhs & rhs)(state)
                else:
                    self.assertEqual((lhs & rhs)(state), expected)
