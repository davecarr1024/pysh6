from typing import Optional
from unittest import TestCase
from pysh.core.parser import results, states


class StateAndOptionalResultTest(TestCase):
    def test_convert(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndOptionalResult[int],
                states.StateAndSingleResult[int],
            ]
        ](
            [
                (
                    states.StateAndOptionalResult[int](
                        states.State(), results.OptionalResult[int]()
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](-1)
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(), results.OptionalResult[int](1)
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](1)
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):

                def convert(result: Optional[int]) -> int:
                    if result is None:
                        return -1
                    else:
                        return result

                self.assertEqual(state_and_result.convert(convert), expected)

    def test_convert_type(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndOptionalResult[str],
                states.StateAndSingleResult[int],
            ]
        ](
            [
                (
                    states.StateAndOptionalResult[str](
                        states.State(), results.OptionalResult[str]()
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](-1)
                    ),
                ),
                (
                    states.StateAndOptionalResult[str](
                        states.State(), results.OptionalResult[str]("1")
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](1)
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):

                def convert(result: Optional[str]) -> int:
                    if result is None:
                        return -1
                    else:
                        return int(result)

                self.assertEqual(state_and_result.convert_type(convert), expected)
