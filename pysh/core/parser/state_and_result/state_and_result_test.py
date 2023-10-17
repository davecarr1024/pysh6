import stat
from typing import Optional
from unittest import TestCase
from pysh.core import tokens
from pysh.core.parser import errors
from pysh.core.parser.state_and_result import *
from pysh.core.parser.state_and_result import state

_Result = int


class StateAndResultTest(TestCase):
    def test_no(self):
        for state_and_result, expected in list[
            tuple[StateAndResult[_Result], Optional[StateAndNoResult[_Result]]]
        ](
            [
                (
                    StateAndNoResult[_Result](state.State()),
                    StateAndNoResult[_Result](state.State()),
                ),
                (
                    StateAndSingleResult[_Result](state.State(), 0),
                    StateAndNoResult[_Result](state.State()),
                ),
                (
                    StateAndOptionalResult[_Result](state.State()),
                    StateAndNoResult[_Result](state.State()),
                ),
                (
                    StateAndMultipleResults[_Result](state.State()),
                    StateAndNoResult[_Result](state.State()),
                ),
                (
                    StateAndNamedResults[_Result](state.State()),
                    StateAndNoResult[_Result](state.State()),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.no()
                else:
                    self.assertEqual(state_and_result.no(), expected)

    def test_single(self):
        for state_and_result, expected in list[
            tuple[StateAndResult[_Result], Optional[StateAndSingleResult[_Result]]]
        ](
            [
                (
                    StateAndNoResult[_Result](state.State()),
                    None,
                ),
                (
                    StateAndSingleResult[_Result](state.State(), 0),
                    StateAndSingleResult[_Result](state.State(), 0),
                ),
                (
                    StateAndOptionalResult[_Result](state.State()),
                    None,
                ),
                (
                    StateAndOptionalResult[_Result](state.State(), 0),
                    StateAndSingleResult[_Result](state.State(), 0),
                ),
                (
                    StateAndMultipleResults[_Result](state.State()),
                    None,
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0]),
                    StateAndSingleResult[_Result](state.State(), 0),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0, 1]),
                    None,
                ),
                (
                    StateAndNamedResults[_Result](state.State()),
                    None,
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                    StateAndSingleResult[_Result](state.State(), 0),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0, "b": 1}),
                    None,
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.single()
                else:
                    self.assertEqual(state_and_result.single(), expected)

    def test_optional(self):
        for state_and_result, expected in list[
            tuple[StateAndResult[_Result], Optional[StateAndOptionalResult[_Result]]]
        ](
            [
                (
                    StateAndNoResult[_Result](state.State()),
                    StateAndOptionalResult[_Result](state.State()),
                ),
                (
                    StateAndOptionalResult[_Result](state.State(), 0),
                    StateAndOptionalResult[_Result](state.State(), 0),
                ),
                (
                    StateAndOptionalResult[_Result](state.State()),
                    StateAndOptionalResult[_Result](state.State()),
                ),
                (
                    StateAndSingleResult[_Result](state.State(), 0),
                    StateAndOptionalResult[_Result](state.State(), 0),
                ),
                (
                    StateAndMultipleResults[_Result](state.State()),
                    StateAndOptionalResult[_Result](state.State()),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0]),
                    StateAndOptionalResult[_Result](state.State(), 0),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0, 1]),
                    None,
                ),
                (
                    StateAndNamedResults[_Result](state.State()),
                    StateAndOptionalResult[_Result](state.State()),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                    StateAndOptionalResult[_Result](state.State(), 0),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0, "b": 1}),
                    None,
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.optional()
                else:
                    self.assertEqual(state_and_result.optional(), expected)

    def test_multiple(self):
        for state_and_result, expected in list[
            tuple[StateAndResult[_Result], Optional[StateAndMultipleResults[_Result]]]
        ](
            [
                (
                    StateAndNoResult[_Result](state.State()),
                    StateAndMultipleResults[_Result](state.State()),
                ),
                (
                    StateAndOptionalResult[_Result](state.State(), 0),
                    StateAndMultipleResults[_Result](state.State(), [0]),
                ),
                (
                    StateAndOptionalResult[_Result](state.State()),
                    StateAndMultipleResults[_Result](state.State()),
                ),
                (
                    StateAndOptionalResult[_Result](state.State(), 0),
                    StateAndMultipleResults[_Result](state.State(), [0]),
                ),
                (
                    StateAndMultipleResults[_Result](state.State()),
                    StateAndMultipleResults[_Result](state.State()),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0]),
                    StateAndMultipleResults[_Result](state.State(), [0]),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0, 1]),
                    StateAndMultipleResults[_Result](state.State(), [0, 1]),
                ),
                (
                    StateAndNamedResults[_Result](state.State()),
                    StateAndMultipleResults[_Result](state.State()),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                    StateAndMultipleResults[_Result](state.State(), [0]),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0, "b": 1}),
                    StateAndMultipleResults[_Result](state.State(), [0, 1]),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.multiple()
                else:
                    self.assertEqual(state_and_result.multiple(), expected)

    def test_named(self):
        for state_and_result, expected in list[
            tuple[StateAndResult[_Result], Optional[StateAndNamedResults[_Result]]]
        ](
            [
                (
                    StateAndNoResult[_Result](state.State()),
                    StateAndNamedResults[_Result](state.State()),
                ),
                (
                    StateAndOptionalResult[_Result](state.State(), 0),
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                ),
                (
                    StateAndOptionalResult[_Result](state.State()),
                    StateAndNamedResults[_Result](state.State()),
                ),
                (
                    StateAndSingleResult[_Result](state.State(), 0),
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                ),
                (
                    StateAndMultipleResults[_Result](state.State()),
                    StateAndNamedResults[_Result](state.State()),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0]),
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                ),
                (
                    StateAndMultipleResults[_Result](state.State(), [0, 1]),
                    None,
                ),
                (
                    StateAndNamedResults[_Result](state.State()),
                    StateAndNamedResults[_Result](state.State()),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                    StateAndNamedResults[_Result](state.State(), {"a": 0}),
                ),
                (
                    StateAndNamedResults[_Result](state.State(), {"a": 0, "b": 1}),
                    StateAndNamedResults[_Result](state.State(), {"a": 0, "b": 1}),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        state_and_result.named("a")
                else:
                    self.assertEqual(state_and_result.named("a"), expected)
