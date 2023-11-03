from typing import Sequence
from unittest import TestCase
from pysh.core.parser import results, states


class StateAndMultipleResultTest(TestCase):
    def test_convert(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndMultipleResult[int],
                states.StateAndSingleResult[int],
            ]
        ](
            [
                (
                    states.StateAndMultipleResult[int](
                        states.State(), results.MultipleResult[int]()
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](0)
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](1)
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](3)
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                self.assertEqual(state_and_result.convert(sum), expected)

    def test_convert_type(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndMultipleResult[str],
                states.StateAndSingleResult[int],
            ]
        ](
            [
                (
                    states.StateAndMultipleResult[str](
                        states.State(), results.MultipleResult[str]()
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](0)
                    ),
                ),
                (
                    states.StateAndMultipleResult[str](
                        states.State(), results.MultipleResult[str](["1"])
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](1)
                    ),
                ),
                (
                    states.StateAndMultipleResult[str](
                        states.State(), results.MultipleResult[str](["1", "2"])
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](3)
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):

                def convert(results: Sequence[str]) -> int:
                    return sum(map(int, results))

                self.assertEqual(state_and_result.convert_type(convert), expected)
