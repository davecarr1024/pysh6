from dataclasses import dataclass
from unittest import TestCase
from pysh.core.parser import rules, states


class NoResultsAndTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        for lhs, rhs, expected in list[
            tuple[
                rules.NoResultsRule[State, int],
                rules.NoResultsRule[State, str],
                states.StateAndNoResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no(),
                    rules.Constant[State, str]("a").no(),
                    states.StateAndNoResults[State, int | str](State()),
                )
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.NoResultsAnd[State, int, str]([lhs, rhs])(State()),
                    expected,
                )
