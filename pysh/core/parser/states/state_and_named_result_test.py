from typing import Optional
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, states


class StateAndNamedResultTest(TestCase):
    def test_convert(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndNamedResult[int],
                Optional[states.StateAndSingleResult[int]],
            ]
        ](
            [
                (
                    states.StateAndNamedResult[int](
                        states.State(), results.NamedResult[int]()
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](12)
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2, "c": 3}),
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):

                def convert(a: int, b: int) -> int:
                    return a * 10 + b

                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.convert(convert)
                else:
                    self.assertEqual(state_and_result.convert(convert), expected)

    def test_convert_type(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndNamedResult[str],
                Optional[states.StateAndSingleResult[int]],
            ]
        ](
            [
                (
                    states.StateAndNamedResult[str](
                        states.State(), results.NamedResult[str]()
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[str](
                        states.State(),
                        results.NamedResult[str]({"a": "1"}),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[str](
                        states.State(),
                        results.NamedResult[str]({"a": "1", "b": "2"}),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(), results.SingleResult[int](12)
                    ),
                ),
                (
                    states.StateAndNamedResult[str](
                        states.State(),
                        results.NamedResult[str]({"a": "1", "b": "2", "c": "3"}),
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):

                def convert_type(a: str, b: str) -> int:
                    return int(a) * 10 + int(b)

                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.convert_type(convert_type)
                else:
                    self.assertEqual(
                        state_and_result.convert_type(convert_type), expected
                    )
