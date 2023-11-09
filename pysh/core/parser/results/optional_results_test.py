from typing import Optional, Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results


class OptionalResultsTest(TestCase):
    def test_no(self):
        self.assertEqual(results.OptionalResults[int]().no(), results.NoResults[int]())
        self.assertEqual(results.OptionalResults[int](1).no(), results.NoResults[int]())

    def test_single(self):
        with self.assertRaises(errors.Error):
            results.OptionalResults[int]().single()
        self.assertEqual(
            results.OptionalResults[int](1).single(), results.SingleResults[int](1)
        )

    def test_optional(self):
        self.assertEqual(
            results.OptionalResults[int]().optional(), results.OptionalResults[int]()
        )
        self.assertEqual(
            results.OptionalResults[int](1).optional(), results.OptionalResults[int](1)
        )

    def test_multiple(self):
        self.assertEqual(
            results.OptionalResults[int]().multiple(),
            results.MultipleResults[int](),
        )
        self.assertEqual(
            results.OptionalResults[int](1).multiple(),
            results.MultipleResults[int]([1]),
        )

    def test_named(self):
        self.assertEqual(
            results.OptionalResults[int]().named(), results.NamedResults[int]()
        )
        self.assertEqual(
            results.OptionalResults[int](1).named(), results.NamedResults[int]({"": 1})
        )

    def test_or_no(self):
        self.assertEqual(
            results.OptionalResults[int]() | results.NoResults[int](),
            results.OptionalResults[int](),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.NoResults[int](),
            results.OptionalResults[int](1),
        )

    def test_or_single(self):
        self.assertEqual(
            results.OptionalResults[int]() | results.SingleResults[int](2),
            results.MultipleResults[int]([2]),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.SingleResults[int](2),
            results.MultipleResults[int]([1, 2]),
        )

    def test_or_optional(self):
        self.assertEqual(
            results.OptionalResults[int]() | results.OptionalResults[int](),
            results.MultipleResults[int](),
        )
        self.assertEqual(
            results.OptionalResults[int]() | results.OptionalResults[int](2),
            results.MultipleResults[int]([2]),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.OptionalResults[int](),
            results.MultipleResults[int]([1]),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.OptionalResults[int](2),
            results.MultipleResults[int]([1, 2]),
        )

    def test_or_multiple(self):
        self.assertEqual(
            results.OptionalResults[int]() | results.MultipleResults[int](),
            results.MultipleResults[int](),
        )
        self.assertEqual(
            results.OptionalResults[int]() | results.MultipleResults[int]([2]),
            results.MultipleResults[int]([2]),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.MultipleResults[int](),
            results.MultipleResults[int]([1]),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.MultipleResults[int]([2]),
            results.MultipleResults[int]([1, 2]),
        )

    def test_or_named(self):
        self.assertEqual(
            results.OptionalResults[int]() | results.NamedResults[int](),
            results.NamedResults[int](),
        )
        self.assertEqual(
            results.OptionalResults[int]() | results.NamedResults[int]({"a": 2}),
            results.NamedResults[int]({"a": 2}),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.NamedResults[int](),
            results.NamedResults[int]({"": 1}),
        )
        self.assertEqual(
            results.OptionalResults[int](1) | results.NamedResults[int]({"a": 2}),
            results.NamedResults[int]({"": 1, "a": 2}),
        )

    def test_convert(self):
        for lhs, expected in list[
            tuple[results.OptionalResults[str], results.SingleResults[int]]
        ](
            [
                (
                    results.OptionalResults[str](),
                    results.SingleResults[int](-1),
                ),
                (
                    results.OptionalResults[str]("1"),
                    results.SingleResults[int](1),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, expected=expected):

                def convert(value: Optional[str]) -> int:
                    if value is None:
                        return -1
                    else:
                        return int(value)

                self.assertEqual(lhs.convert(convert), expected)

    def test_or_type(self):
        for lhs, rhs, expected in list[
            tuple[
                results.OptionalResults[int],
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
                    results.OptionalResults[int](),
                    results.NoResults[str](),
                    results.OptionalResults[int | str](),
                ),
                (
                    results.OptionalResults[int](1),
                    results.NoResults[str](),
                    results.OptionalResults[int | str](1),
                ),
                (
                    results.OptionalResults[int](),
                    results.SingleResults[str]("a"),
                    results.MultipleResults[int | str](["a"]),
                ),
                (
                    results.OptionalResults[int](1),
                    results.SingleResults[str]("a"),
                    results.MultipleResults[int | str]([1, "a"]),
                ),
                (
                    results.OptionalResults[int](),
                    results.OptionalResults[str](),
                    results.MultipleResults[int | str](),
                ),
                (
                    results.OptionalResults[int](1),
                    results.OptionalResults[str](),
                    results.MultipleResults[int | str]([1]),
                ),
                (
                    results.OptionalResults[int](),
                    results.OptionalResults[str]("a"),
                    results.MultipleResults[int | str](["a"]),
                ),
                (
                    results.OptionalResults[int](1),
                    results.OptionalResults[str]("a"),
                    results.MultipleResults[int | str]([1, "a"]),
                ),
                (
                    results.OptionalResults[int](),
                    results.MultipleResults[str](),
                    results.MultipleResults[int | str](),
                ),
                (
                    results.OptionalResults[int](1),
                    results.MultipleResults[str](),
                    results.MultipleResults[int | str]([1]),
                ),
                (
                    results.OptionalResults[int](),
                    results.MultipleResults[str](["a"]),
                    results.MultipleResults[int | str](["a"]),
                ),
                (
                    results.OptionalResults[int](1),
                    results.MultipleResults[str](["a"]),
                    results.MultipleResults[int | str]([1, "a"]),
                ),
                (
                    results.OptionalResults[int](),
                    results.NamedResults[str](),
                    results.NamedResults[int | str](),
                ),
                (
                    results.OptionalResults[int](1),
                    results.NamedResults[str](),
                    results.NamedResults[int | str]({"": 1}),
                ),
                (
                    results.OptionalResults[int](1),
                    results.NamedResults[str]({"a": "v"}),
                    results.NamedResults[int | str]({"": 1, "a": "v"}),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
