from typing import Optional
from unittest import TestCase
from pysh.core.parser import results


class OptionalResultTest(TestCase):
    def test_no(self):
        for result, expected in list[
            tuple[results.OptionalResult[int], results.NoResult[int]]
        ](
            [
                (results.OptionalResult[int](), results.NoResult[int]()),
                (results.OptionalResult[int](1), results.NoResult[int]()),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                self.assertEqual(result.no(), expected)

    def test_single(self):
        for result, expected in list[
            tuple[results.OptionalResult[int], Optional[results.SingleResult[int]]]
        ](
            [
                (results.OptionalResult[int](), None),
                (results.OptionalResult[int](1), results.SingleResult[int](1)),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        result.single()
                else:
                    self.assertEqual(result.single(), expected)

    def test_optional(self):
        for result, expected in list[
            tuple[results.OptionalResult[int], Optional[results.OptionalResult[int]]]
        ](
            [
                (results.OptionalResult[int](), results.OptionalResult[int]()),
                (results.OptionalResult[int](1), results.OptionalResult[int](1)),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        result.optional()
                else:
                    self.assertEqual(result.optional(), expected)

    def test_multiple(self):
        for result, expected in list[
            tuple[results.OptionalResult[int], Optional[results.MultipleResult[int]]]
        ](
            [
                (results.OptionalResult[int](), results.MultipleResult[int]()),
                (results.OptionalResult[int](1), results.MultipleResult[int]([1])),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        result.multiple()
                else:
                    self.assertEqual(result.multiple(), expected)

    def test_named(self):
        for result, expected in list[
            tuple[results.OptionalResult[int], Optional[results.NamedResult[int]]]
        ](
            [
                (results.OptionalResult[int](), results.NamedResult[int]()),
                (results.OptionalResult[int](1), results.NamedResult[int]({"a": 1})),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        result.named("a")
                else:
                    self.assertEqual(result.named("a"), expected)

    def test_convert(self):
        for result, expected in list[
            tuple[results.OptionalResult[int], results.SingleResult[int]]
        ](
            [
                (results.OptionalResult[int](), results.SingleResult[int](-1)),
                (results.OptionalResult[int](1), results.SingleResult[int](2)),
            ]
        ):
            with self.subTest(result=result, expected=expected):

                def convert(result: Optional[int]) -> int:
                    if result is None:
                        return -1
                    else:
                        return result * 2

                self.assertEqual(
                    result.convert_type(convert),
                    expected,
                )

    def test_or(self):
        for lhs, rhs, expected in list[
            tuple[results.OptionalResult[int], results.OrArgs, results.Results[int]]
        ](
            [
                (
                    results.OptionalResult[int](),
                    results.NoResult[int](),
                    results.OptionalResult[int](),
                ),
                (
                    results.OptionalResult[int](0),
                    results.NoResult[int](),
                    results.OptionalResult[int](0),
                ),
                (
                    results.OptionalResult[int](),
                    results.SingleResult[int](1),
                    results.MultipleResult[int]([1]),
                ),
                (
                    results.OptionalResult[int](0),
                    results.SingleResult[int](1),
                    results.MultipleResult[int]([0, 1]),
                ),
                (
                    results.OptionalResult[int](),
                    results.OptionalResult[int](),
                    results.MultipleResult[int](),
                ),
                (
                    results.OptionalResult[int](0),
                    results.OptionalResult[int](),
                    results.MultipleResult[int]([0]),
                ),
                (
                    results.OptionalResult[int](),
                    results.OptionalResult[int](1),
                    results.MultipleResult[int]([1]),
                ),
                (
                    results.OptionalResult[int](0),
                    results.OptionalResult[int](1),
                    results.MultipleResult[int]([0, 1]),
                ),
                (
                    results.OptionalResult[int](),
                    results.MultipleResult[int]([1]),
                    results.MultipleResult[int]([1]),
                ),
                (
                    results.OptionalResult[int](0),
                    results.MultipleResult[int]([1]),
                    results.MultipleResult[int]([0, 1]),
                ),
                (
                    results.OptionalResult[int](),
                    results.NamedResult[int]({"a": 1}),
                    results.NamedResult[int]({"a": 1}),
                ),
                (
                    results.OptionalResult[int](0),
                    results.NamedResult[int]({"a": 1}),
                    results.NamedResult[int]({"": 0, "a": 1}),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
