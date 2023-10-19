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
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int](),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
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
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int](),
                    ),
                    None,
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
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
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int](),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
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
                Optional[states.StateAndMultipleResults[int]],
            ]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([]),
                    ),
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([]),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int](),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([]),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([]),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
                    ),
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
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
            tuple[
                states.StateAndResult[int], Optional[states.StateAndNamedResults[int]]
            ]
        ](
            [
                (
                    states.StateAndNoResult[int](
                        states.State(),
                        results.NoResult[int](),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                ),
                (
                    states.StateAndSingleResult[int](
                        states.State(),
                        results.SingleResult[int](1),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                ),
                (
                    states.StateAndOptionalResult[int](
                        states.State(),
                        results.OptionalResult[int](1),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int](),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1]),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndMultipleResults[int](
                        states.State(),
                        results.MultipleResults[int]([1, 2]),
                    ),
                    None,
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int](),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1}),
                    ),
                ),
                (
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
                    ),
                    states.StateAndNamedResults[int](
                        states.State(),
                        results.NamedResults[int]({"a": 1, "b": 2}),
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
