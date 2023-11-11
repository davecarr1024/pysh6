from dataclasses import dataclass
from unittest import TestCase
from pysh.core.parser import results, states
from pysh.core.parser.rules import constant


class ConstantTest(TestCase):
    def test_call(self):
        @dataclass(frozen=True)
        class State:
            ...

        self.assertEqual(
            constant.Constant[State, int](1)(State()),
            states.StateAndSingleResults[State, int](
                State(),
                results.SingleResults[int](1),
            ),
        )
