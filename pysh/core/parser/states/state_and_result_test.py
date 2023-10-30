from typing import Optional
from unittest import TestCase
from pysh.core.parser import results, states


class StateAndResultTest(TestCase):
    def test_no(self):
        for state_and_result, expected in list[
            tuple[states.StateAndResult[int], states.StateAndNoResult[int]]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int](),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                self.assertEqual(state_and_result.no(), expected)

    def test_single(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndResult[int], Optional[states.StateAndSingleResult[int]]
            ]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    None,
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    None,
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int](),
                    ),
                    None,
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        state_and_result.single()
                else:
                    self.assertEqual(state_and_result.single(), expected)

    def test_optional(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndResult[int], Optional[states.StateAndOptionalResult[int]]
            ]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int](),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                    None,
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        state_and_result.optional()
                else:
                    self.assertEqual(state_and_result.optional(), expected)

    def test_multiple(self):
        for state_and_result, expected in list[
            tuple[
                states.StateAndResult[int],
                Optional[states.StateAndMultipleResult[int]],
            ]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([]),
                    ),
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([]),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int](),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([]),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([]),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        state_and_result.multiple()
                else:
                    self.assertEqual(state_and_result.multiple(), expected)

    def test_named(self):
        for state_and_result, expected in list[
            tuple[states.StateAndResult[int], Optional[states.StateAndNamedResult[int]]]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int](),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1]),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndMultipleResult[int](
                        states.State(),
                        results.MultipleResult[int]([1, 2]),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                    states.StateAndNamedResult[int](
                        states.State(),
                        results.NamedResult[int]({"a": 1, "b": 2}),
                    ),
                ),
            ]
        ):
            with self.subTest(state_and_result=state_and_result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        state_and_result.named("a")
                else:
                    self.assertEqual(state_and_result.named("a"), expected)
