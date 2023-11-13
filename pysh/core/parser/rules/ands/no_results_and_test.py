from dataclasses import dataclass
from unittest import TestCase
from pysh.core.parser import rules, states


class NoResultsAndTest(TestCase):
    def test_call(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                rules.NoResultsRule[states.State, int],
                rules.NoResultsRule[states.State, str],
                states.StateAndNoResults[states.State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).no(),
                    rules.Constant[states.State, str]("a").no(),
                    states.StateAndNoResults[states.State, int | str](states.State()),
                )
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.NoResultsAnd[states.State, int, str]([lhs, rhs])(
                        states.State()
                    ),
                    expected,
                )
