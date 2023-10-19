from typing import Optional
from unittest import TestCase
from pysh.core.parser import results


class MultipleResultTest(TestCase):
    def test_no(self):
        for result, expected in list[
            tuple[results.MultipleResults[int], results.NoResult[int]]
        ](
            [
                (results.MultipleResults[int](), results.NoResult[int]()),
                (results.MultipleResults[int]([1]), results.NoResult[int]()),
                (results.MultipleResults[int]([1, 2]), results.NoResult[int]()),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                self.assertEqual(result.no(), expected)

    def test_single(self):
        for result, expected in list[
            tuple[results.MultipleResults[int], Optional[results.SingleResult[int]]]
        ](
            [
                (results.MultipleResults[int](), None),
                (results.MultipleResults[int]([1]), results.SingleResult[int](1)),
                (results.MultipleResults[int]([1, 2]), None),
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
            tuple[results.MultipleResults[int], Optional[results.OptionalResult[int]]]
        ](
            [
                (results.MultipleResults[int](), results.OptionalResult[int]()),
                (results.MultipleResults[int]([1]), results.OptionalResult[int](1)),
                (results.MultipleResults[int]([1, 2]), None),
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
            tuple[results.MultipleResults[int], Optional[results.MultipleResults[int]]]
        ](
            [
                (results.MultipleResults[int](), results.MultipleResults[int]()),
                (results.MultipleResults[int]([1]), results.MultipleResults[int]([1])),
                (
                    results.MultipleResults[int]([1, 2]),
                    results.MultipleResults[int]([1, 2]),
                ),
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
            tuple[results.MultipleResults[int], Optional[results.NamedResults[int]]]
        ](
            [
                (results.MultipleResults[int](), results.NamedResults[int]()),
                (
                    results.MultipleResults[int]([1]),
                    results.NamedResults[int]({"a": 1}),
                ),
                (results.MultipleResults[int]([1, 1]), None),
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
            tuple[results.MultipleResults[int], results.SingleResult[int]]
        ](
            [
                (results.MultipleResults[int](), results.SingleResult[int](0)),
                (results.MultipleResults[int]([1]), results.SingleResult[int](1)),
                (results.MultipleResults[int]([1, 2]), results.SingleResult[int](3)),
            ]
        ):
            with self.subTest(result=result, expected=expected):
                self.assertEqual(
                    result.convert(lambda r: results.SingleResult[int](sum(r))),
                    expected,
                )
