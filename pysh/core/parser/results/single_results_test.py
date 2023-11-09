from typing import Union
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

    def test_convert(self):
        self.assertEqual(
            results.SingleResults[str]("1").convert(int), results.SingleResults[int](1)
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
                    results.SingleResults[int | str](1),
                ),
                (
                    results.SingleResults[str]("a"),
                    results.MultipleResults[int | str]([1, "a"]),
                ),
                (
                    results.OptionalResults[str](),
                    results.MultipleResults[int | str]([1]),
                ),
                (
                    results.OptionalResults[str]("a"),
                    results.MultipleResults[int | str]([1, "a"]),
                ),
                (
                    results.MultipleResults[str](),
                    results.MultipleResults[int | str]([1]),
                ),
                (
                    results.MultipleResults[str](["a"]),
                    results.MultipleResults[int | str]([1, "a"]),
                ),
                (
                    results.NamedResults[str](),
                    results.NamedResults[int | str]({"": 1}),
                ),
                (
                    results.NamedResults[str]({"a": "v"}),
                    results.NamedResults[int | str]({"": 1, "a": "v"}),
                ),
            ]
        ):
            with self.subTest(rhs=rhs, expected=expected):
                lhs = results.SingleResults[int](1)
                self.assertEqual(lhs | rhs, expected)
