from dataclasses import dataclass
from typing import Optional
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class SingleResultsOrTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        def fail(_):
            raise errors.Error()

        for lhs, rhs, expected in list[
            tuple[
                rules.SingleResultsRule[State, int]
                | rules.SingleResultsRule[State, str],
                rules.SingleResultsRule[State, int]
                | rules.SingleResultsRule[State, str],
                Optional[states.StateAndSingleResults[State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).convert(fail),
                    rules.Constant[State, int](1).convert(fail),
                    None,
                ),
                (
                    rules.Constant[State, int](1).convert(fail),
                    rules.Constant[State, int](1),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[State, int](1).convert(fail),
                    rules.Constant[State, str]("a"),
                    states.StateAndSingleResults[State, int | str](
                        State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                rule = rules.ors.SingleResultsOr[State, int, str]([lhs, rhs])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(State())
                else:
                    self.assertEqual(rule(State()), expected)
