from unittest import TestCase
from pysh.core.parser import results, states


class StateAndNoResultTest(TestCase):
    def test_convert(self):
        self.assertEqual(
            states.StateAndNoResult[int](
                states.State(), results.NoResult[int]()
            ).convert(lambda: 1),
            states.StateAndSingleResult[int](
                states.State(), results.SingleResult[int](1)
            ),
        )

    def test_convert_type(self):
        self.assertEqual(
            states.StateAndNoResult[str](
                states.State(), results.NoResult[str]()
            ).convert_type(lambda: 1),
            states.StateAndSingleResult[int](
                states.State(), results.SingleResult[int](1)
            ),
        )
