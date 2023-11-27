from dataclasses import dataclass
from typing import Optional
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class SingleResultsOrTest(TestCase):
    def test_call(self) -> None:
        def fail(_):
            raise rules.Rule._cls_error()

        for lhs, rhs, expected in list[
            tuple[
                rules.SingleResultsRule[states.State, int]
                | rules.SingleResultsRule[states.State, str],
                rules.SingleResultsRule[states.State, int]
                | rules.SingleResultsRule[states.State, str],
                Optional[states.StateAndSingleResults[states.State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).convert(fail),
                    rules.Constant[states.State, int](1).convert(fail),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1).convert(fail),
                    rules.Constant[states.State, int](1),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str](1),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1).convert(fail),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndSingleResults[states.State, int | str](
                        states.State(),
                        results.SingleResults[int | str]("a"),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                rule = rules.ors.SingleResultsOr[states.State, int, str]([lhs, rhs])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(states.State())
                else:
                    self.assertEqual(rule(states.State()), expected)
