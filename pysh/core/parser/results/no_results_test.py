from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results


class NoResultsTest(TestCase):
    def test_no(self):
        self.assertEqual(results.NoResults[int](), results.NoResults[int]())

    def test_single(self):
        with self.assertRaises(errors.Error):
            results.NoResults[int]().single()

    def test_optional(self):
        self.assertEqual(
            results.NoResults[int]().optional(), results.OptionalResults[int]()
        )

    def test_multiple(self):
        self.assertEqual(
            results.NoResults[int]().multiple(), results.MultipleResults[int]()
        )

    def test_named(self):
        self.assertEqual(results.NoResults[int]().named(), results.NamedResults[int]())
        self.assertEqual(
            results.NoResults[int]().named("a"), results.NamedResults[int]()
        )

    def test_or_no(self):
        self.assertEqual(
            results.NoResults[int]() | results.NoResults[int](),
            results.NoResults[int](),
        )

    def test_or_single(self):
        self.assertEqual(
            results.NoResults[int]() | results.SingleResults[int](1),
            results.SingleResults[int](1),
        )

    def test_or_optional(self):
        self.assertEqual(
            results.NoResults[int]() | results.OptionalResults[int](),
            results.OptionalResults[int](),
        )
        self.assertEqual(
            results.NoResults[int]() | results.OptionalResults[int](1),
            results.OptionalResults[int](1),
        )

    def test_or_multiple(self):
        self.assertEqual(
            results.NoResults[int]() | results.MultipleResults[int](),
            results.MultipleResults[int](),
        )
        self.assertEqual(
            results.NoResults[int]() | results.MultipleResults[int]([1]),
            results.MultipleResults[int]([1]),
        )

    def test_or_named(self):
        self.assertEqual(
            results.NoResults[int]() | results.NamedResults[int](),
            results.NamedResults[int](),
        )
        self.assertEqual(
            results.NoResults[int]() | results.NamedResults[int]({"a": 1}),
            results.NamedResults[int]({"a": 1}),
        )

    def test_convert(self):
        self.assertEqual(
            results.NoResults[str]().convert(lambda: 1), results.SingleResults[int](1)
        )
