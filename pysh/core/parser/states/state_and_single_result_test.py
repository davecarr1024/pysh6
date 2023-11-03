from unittest import TestCase
from pysh.core.parser import results, states


class StateAndSingleResultTest(TestCase):
    def test_convert(self):
        self.assertEqual(
            states.StateAndSingleResult[int](
                states.State(), results.SingleResult[int](1)
            ).convert(lambda result: result * 2),
            states.StateAndSingleResult[int](
                states.State(), results.SingleResult[int](2)
            ),
        )

    def test_convert_type(self):
        self.assertEqual(
            states.StateAndSingleResult[str](
                states.State(), results.SingleResult[str]("1")
            ).convert_type(int),
            states.StateAndSingleResult[int](
                states.State(), results.SingleResult[int](1)
            ),
        )
