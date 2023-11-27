from dataclasses import dataclass
from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class OptionalResultsOrTest(TestCase):
    def test_call(self) -> None:
        def fail(_):
            raise rules.Rule._cls_error()

        for lhs, rhs, expected in list[
            tuple[
                Union[
                    rules.NoResultsRule[states.State, int],
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, int],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, int],
                    rules.OptionalResultsRule[states.State, str],
                ],
                Union[
                    rules.NoResultsRule[states.State, int],
                    rules.NoResultsRule[states.State, str],
                    rules.SingleResultsRule[states.State, int],
                    rules.SingleResultsRule[states.State, str],
                    rules.OptionalResultsRule[states.State, int],
                    rules.OptionalResultsRule[states.State, str],
                ],
                Optional[states.StateAndOptionalResults[states.State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).optional().convert(fail),
                    rules.Constant[states.State, int](2).optional().convert(fail),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1).optional().convert(fail),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional().convert(fail),
                    rules.Constant[states.State, str]("a").no().optional(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional().convert(fail),
                    rules.Constant[states.State, str]("a").optional(),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).optional().convert(fail),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndOptionalResults[states.State, int | str](
                        states.State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                rule = rules.ors.OptionalResultsOr[states.State, int, str]([lhs, rhs])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(states.State())
                else:
                    self.assertEqual(rule(states.State()), expected)
