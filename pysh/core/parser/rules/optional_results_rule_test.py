from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class NoResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        def convert(value: Optional[str]) -> int:
            return int(value) if value is not None else -1

        self.assertEqual(
            rules.Constant[states.State, str]("1")
            .optional()
            .convert(convert)(states.State()),
            states.StateAndSingleResults[states.State, int](
                states.State(), results.SingleResults[int](1)
            ),
        )

    def test_and(self) -> None:
        for lhs, rhs, state, expected in list[
            tuple[
                rules.OptionalResultsRule[states.State, int],
                Union[
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, str],
                    rules.MultipleResultsRule[states.State, str],
                    rules.NamedResultsRule[states.State, str],
                    str,
                ],
                states.State,
                Optional[states.StateAndResults[states.State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State()
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a").no(),
                    states.State(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    "a",
                    states.State(),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
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
                    states.StateAndOptionalResults[states.State, int](states.State()),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
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
                    rules.Constant[states.State, int](1).optional(),
                    "a",
                    states.State(),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
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
                    states.StateAndOptionalResults[states.State, int](
                        states.State(),
                        results.OptionalResults[int](1),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
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
