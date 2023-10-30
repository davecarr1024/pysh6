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
            tuple[results.OptionalResult[int], Optional[results.MultipleResults[int]]]
        ](
            [
                (results.OptionalResult[int](), results.MultipleResults[int]()),
                (results.OptionalResult[int](1), results.MultipleResults[int]([1])),
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
            tuple[results.OptionalResult[int], Optional[results.NamedResults[int]]]
        ](
            [
                (results.OptionalResult[int](), results.NamedResults[int]()),
                (results.OptionalResult[int](1), results.NamedResults[int]({"a": 1})),
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
                self.assertEqual(
                    result.convert(
                        lambda r: results.SingleResult[int](r.result * 2)
                        if r.result is not None
                        else results.SingleResult[int](-1)
                    ),
                    expected,
                )