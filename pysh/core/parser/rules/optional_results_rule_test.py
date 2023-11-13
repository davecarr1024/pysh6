from typing import Optional, Union
from unittest import TestCase
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
        for lhs, rhs, expected in list[
            tuple[
                rules.OptionalResultsRule[states.State, int],
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
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State()
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).no().optional(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional(),
                    rules.Constant[states.State, str]("a").optional(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1, "a"]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual((lhs & rhs)(states.State()), expected)
