from typing import Optional
from unittest import TestCase
from pysh.core.parser import results


class OptionalResultTest(TestCase):
    def test_no(self):
        for result, expected in list[tuple[results.OptionalResult[int],results.NoResult[int]]]([
(results.OptionalResult[int](), results.NoResult[int]()),
(results.OptionalResult[int](0), results.NoResult[int]())
        ]):
            with self.subTest(results=result,expected=expected):
                self.assertEqual(result.no(),expected)

    def test_single(self):
        for result, expected in list[tuple[results.OptionalResult[int],Optional[results.SingleResult[int]]]]([
(results.OptionalResult[int](), None),
(results.OptionalResult[int](0), results.SingleResult[int](0))
        ]):
            with self.subTest(results=result,expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        result.single()
                else:
                    self.assertEqual(result.single(),expected)

    def test_optional(self):
        self.assertEqual(
            results.OptionalResult[int](0).optional(), results.OptionalResult[int](0)
        )

    def test_multiple(self):
        self.assertEqual(
            results.OptionalResult[int](0).multiple(), results.MultipleResults[int]([0])
        )

    def test_named(self):
        self.assertEqual(
            results.OptionalResult[int](0).named("a"), results.NamedResults[int]({"a": 0})
        )

    def test_convert(self):
        self.assertEqual(
            results.OptionalResult[int](1).convert(
                lambda r: results.OptionalResult[int](r.result * 2)
            ),
            results.OptionalResult[int](2),
        )
