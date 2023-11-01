from unittest import TestCase
from pysh.core.parser import results


class SingleResultTest(TestCase):
    def test_no(self):
        self.assertEqual(results.SingleResult[int](0).no(), results.NoResult[int]())

    def test_single(self):
        self.assertEqual(
            results.SingleResult[int](0).single(), results.SingleResult[int](0)
        )

    def test_optional(self):
        self.assertEqual(
            results.SingleResult[int](0).optional(), results.OptionalResult[int](0)
        )

    def test_multiple(self):
        self.assertEqual(
            results.SingleResult[int](0).multiple(), results.MultipleResult[int]([0])
        )

    def test_named(self):
        self.assertEqual(
            results.SingleResult[int](0).named("a"), results.NamedResult[int]({"a": 0})
        )

    def test_convert(self):
        def convert(result: int) -> int:
            return result * 2

        self.assertEqual(
            results.SingleResult[int](1).convert(convert),
            results.SingleResult[int](2),
        )

    def test_or(self):
        for lhs, rhs, expected in list[
            tuple[results.SingleResult[int], results.OrArgs, results.Results[int]]
        ](
            [
                (
                    results.SingleResult[int](0),
                    results.NoResult[int](),
                    results.SingleResult[int](0),
                ),
                (
                    results.SingleResult[int](0),
                    results.SingleResult[int](1),
                    results.MultipleResult[int]([0, 1]),
                ),
                (
                    results.SingleResult[int](0),
                    results.OptionalResult[int](),
                    results.MultipleResult[int]([0]),
                ),
                (
                    results.SingleResult[int](0),
                    results.OptionalResult[int](1),
                    results.MultipleResult[int]([0, 1]),
                ),
                (
                    results.SingleResult[int](0),
                    results.MultipleResult[int]([1]),
                    results.MultipleResult[int]([0, 1]),
                ),
                (
                    results.SingleResult[int](0),
                    results.NamedResult[int]({"a": 1}),
                    results.NamedResult[int]({"": 0, "a": 1}),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
