from typing import Union
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
        self.assertEqual(
            results.SingleResults[int](1) | results.SingleResults[str]("a"),
            results.MultipleResults[int | str]([1, "a"]),
        )

    def test_or_type(self):
        for rhs, expected in list[
            tuple[
                Union[
                    results.NoResults[str],
                    results.SingleResults[str],
                    results.OptionalResults[str],
                    results.MultipleResults[str],
                    results.NamedResults[str],
                ],
                results.Results[int | str],
            ]
        ](
            [
                (
                    results.NoResults[str](),
                    results.NoResults[int | str](),
                ),
                (
                    results.SingleResults[str]("a"),
                    results.SingleResults[int | str]("a"),
                ),
                (
                    results.OptionalResults[str](),
                    results.OptionalResults[int | str](),
                ),
                (
                    results.OptionalResults[str]("a"),
                    results.OptionalResults[int | str]("a"),
                ),
                (
                    results.MultipleResults[str](),
                    results.MultipleResults[int | str](),
                ),
                (
                    results.MultipleResults[str](["a"]),
                    results.MultipleResults[int | str](["a"]),
                ),
                (
                    results.NamedResults[str](),
                    results.NamedResults[int | str](),
                ),
                (
                    results.NamedResults[str]({"a": "v"}),
                    results.NamedResults[int | str]({"a": "v"}),
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected=expected):
                lhs = results.NoResults[int]()
                self.assertEqual(lhs | rhs, expected)
