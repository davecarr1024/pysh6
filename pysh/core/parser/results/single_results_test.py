from unittest import TestCase
from pysh.core.parser import results


class SingleResultsTest(TestCase):
    def test_no(self):
        self.assertEqual(results.SingleResults[int](1).no(), results.NoResults[int]())

    def test_single(self):
        self.assertEqual(
            results.SingleResults[int](1).single(), results.SingleResults[int](1)
        )

    def test_optional(self):
        self.assertEqual(
            results.SingleResults[int](1).optional(), results.OptionalResults[int](1)
        )

    def test_multiple(self):
        self.assertEqual(
            results.SingleResults[int](1).multiple(), results.MultipleResults[int]([1])
        )

    def test_named(self):
        self.assertEqual(
            results.SingleResults[int](1).named(), results.NamedResults[int]({"": 1})
        )
        self.assertEqual(
            results.SingleResults[int](1).named("a"),
            results.NamedResults[int]({"a": 1}),
        )

    def test_or_no(self):
        self.assertEqual(
            results.SingleResults[int](1) | results.NoResults[int](),
            results.SingleResults[int](1),
        )

    def test_or_single(self):
        self.assertEqual(
            results.SingleResults[int](1) | results.SingleResults[int](2),
            results.MultipleResults[int]([1, 2]),
        )

    def test_or_optional(self):
        self.assertEqual(
            results.SingleResults[int](1) | results.OptionalResults[int](),
            results.MultipleResults[int]([1]),
        )
        self.assertEqual(
            results.SingleResults[int](1) | results.OptionalResults[int](2),
            results.MultipleResults[int]([1, 2]),
        )

    def test_or_multiple(self):
        self.assertEqual(
            results.SingleResults[int](1) | results.MultipleResults[int](),
            results.MultipleResults[int]([1]),
        )
        self.assertEqual(
            results.SingleResults[int](1) | results.MultipleResults[int]([2]),
            results.MultipleResults[int]([1, 2]),
        )

    def test_or_named(self):
        self.assertEqual(
            results.SingleResults[int](1) | results.NamedResults[int](),
            results.NamedResults[int]({"": 1}),
        )
        self.assertEqual(
            results.SingleResults[int](1) | results.NamedResults[int]({"a": 2}),
            results.NamedResults[int]({"": 1, "a": 2}),
        )
