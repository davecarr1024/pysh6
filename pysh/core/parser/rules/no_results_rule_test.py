from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


class NoResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        self.assertEqual(
            rules.Constant[states.State, str]("1")
            .no()
            .convert(lambda: 1)(states.State()),
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
                    states.StateAndNoResults[states.State, int | str](states.State()),
                ),
                (
                    rules.Constant[states.State, str]("a"),
                    states.State(),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.State(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").optional(),
                    states.State(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().multiple(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").multiple(),
                    states.State(),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").no().named(),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, str]("a").named("v"),
                    states.State(),
                    states.StateAndNamedResults[states.State, int | str](
                        states.State(),
                        results.NamedResults[int | str]({"v": "a"}),
                    ),
                ),
                (
                    "a",
                    states.State(),
                    None,
                ),
                (
                    "a",
                    states.State(lexer.Result(tokens.Stream([tokens.Token("a", "a")]))),
                    states.StateAndNoResults[states.State, int | str](states.State()),
                ),
                (
                    "b",
                    states.State(lexer.Result(tokens.Stream([tokens.Token("a", "a")]))),
                    None,
                ),
            ]
        ):
            with self.subTest(rhs=rhs, state=state, expected=expected):
                lhs: rules.NoResultsRule[states.State, int] = rules.Constant[
                    states.State, int
                ](1).no()
                if expected is None:
                    with self.assertRaises(errors.Error):
                        (lhs & rhs)(state)
                else:
                    self.assertEqual((lhs & rhs)(state), expected)
