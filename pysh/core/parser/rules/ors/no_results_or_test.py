from dataclasses import dataclass
from unittest import TestCase
from pysh.core.parser import rules, states


class NoResultsOrTest(TestCase):
    def test_call(self):
        @dataclass(frozen=True)
        class State:
            ...

        self.assertEqual(
            rules.ors.NoResultsOr[State, int, str](
                [
                    rules.Constant[State, int](1).no(),
                    rules.Constant[State, str]("a").no(),
                ]
            )(State()),
            states.StateAndNoResults[State, int | str](State()),
        )
