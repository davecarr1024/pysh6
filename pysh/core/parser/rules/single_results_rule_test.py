from dataclasses import dataclass
from unittest import TestCase
from pysh.core.parser import results, rules, states


class NoResultsRuleTest(TestCase):
    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        self.assertEqual(
            rules.Constant[State, str]("1").convert(int)(State()),
            states.StateAndSingleResults[State, int](
                State(), results.SingleResults[int](1)
            ),
        )
