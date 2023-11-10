from dataclasses import dataclass
from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class OptionalResultsOrTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        def fail(_):
            raise errors.Error()

        for lhs, rhs, expected in list[
            tuple[
                Union[
                    rules.NoResultsRule[State, int],
                    rules.NoResultsRule[State, str],
                    rules.SingleResultsRule[State, int],
                    rules.SingleResultsRule[State, str],
                    rules.OptionalResultsRule[State, int],
                    rules.OptionalResultsRule[State, str],
                ],
                Union[
                    rules.NoResultsRule[State, int],
                    rules.NoResultsRule[State, str],
                    rules.SingleResultsRule[State, int],
                    rules.SingleResultsRule[State, str],
                    rules.OptionalResultsRule[State, int],
                    rules.OptionalResultsRule[State, str],
                ],
                Optional[states.StateAndOptionalResults[State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).optional().convert(fail),
                    rules.Constant[State, int](2).optional().convert(fail),
                    None,
                ),
                (
                    rules.Constant[State, int](1).optional().convert(fail),
                    rules.Constant[State, str]("a").no(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional().convert(fail),
                    rules.Constant[State, str]("a").no().optional(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional().convert(fail),
                    rules.Constant[State, str]("a").optional(),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
                (
                    rules.Constant[State, int](1).optional().convert(fail),
                    rules.Constant[State, str]("a"),
                    states.StateAndOptionalResults[State, int | str](
                        State(),
                        results.OptionalResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                rule = rules.ors.OptionalResultsOr[State, int, str]([lhs, rhs])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(State())
                else:
                    self.assertEqual(rule(State()), expected)
