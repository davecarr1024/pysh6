from dataclasses import dataclass
from typing import Union
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results


class NamedResultsTest(TestCase):
    def test_no(self):
        self.assertEqual(results.NamedResults[int]().no(), results.NoResults[int]())
        self.assertEqual(
            results.NamedResults[int]({"a": 1}).no(), results.NoResults[int]()
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2}).no(), results.NoResults[int]()
        )

    def test_single(self):
        with self.assertRaises(errors.Error):
            results.NamedResults[int]().single()
        self.assertEqual(
            results.NamedResults[int]({"a": 1}).single(), results.SingleResults[int](1)
        )
        with self.assertRaises(errors.Error):
            results.NamedResults[int]({"a": 1, "b": 2}).single()

    def test_optional(self):
        self.assertEqual(
            results.NamedResults[int]().optional(), results.OptionalResults[int]()
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}).optional(),
            results.OptionalResults[int](1),
        )
        with self.assertRaises(errors.Error):
            results.NamedResults[int]({"a": 1, "b": 2}).optional()

    def test_multiple(self):
        self.assertEqual(
            results.NamedResults[int]().multiple(),
            results.MultipleResults[int](),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}).multiple(),
            results.MultipleResults[int]([1]),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2}).multiple(),
            results.MultipleResults[int]([1, 2]),
        )

    def test_named(self):
        self.assertEqual(
            results.NamedResults[int]().named(), results.NamedResults[int]()
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}).named(),
            results.NamedResults[int]({"a": 1}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2}).named(),
            results.NamedResults[int]({"a": 1, "b": 2}),
        )
        self.assertEqual(
            results.NamedResults[int]().named("c"), results.NamedResults[int]()
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}).named("c"),
            results.NamedResults[int]({"a": 1}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2}).named("c"),
            results.NamedResults[int]({"a": 1, "b": 2}),
        )

    def test_or_no(self):
        self.assertEqual(
            results.NamedResults[int]() | results.NoResults[int](),
            results.NamedResults[int](),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.NoResults[int](),
            results.NamedResults[int]({"a": 1}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2}) | results.NoResults[int](),
            results.NamedResults[int]({"a": 1, "b": 2}),
        )

    def test_or_single(self):
        self.assertEqual(
            results.NamedResults[int]() | results.SingleResults[int](3),
            results.NamedResults[int]({"": 3}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.SingleResults[int](3),
            results.NamedResults[int]({"a": 1, "": 3}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2}) | results.SingleResults[int](3),
            results.NamedResults[int]({"a": 1, "b": 2, "": 3}),
        )

    def test_or_optional(self):
        self.assertEqual(
            results.NamedResults[int]() | results.OptionalResults[int](),
            results.NamedResults[int](),
        )
        self.assertEqual(
            results.NamedResults[int]() | results.OptionalResults[int](3),
            results.NamedResults[int]({"": 3}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.OptionalResults[int](),
            results.NamedResults[int]({"a": 1}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.OptionalResults[int](3),
            results.NamedResults[int]({"a": 1, "": 3}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2})
            | results.OptionalResults[int](),
            results.NamedResults[int]({"a": 1, "b": 2}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1, "b": 2})
            | results.OptionalResults[int](3),
            results.NamedResults[int]({"a": 1, "b": 2, "": 3}),
        )

    def test_or_multiple(self):
        self.assertEqual(
            results.NamedResults[int]() | results.MultipleResults[int](),
            results.NamedResults[int](),
        )
        self.assertEqual(
            results.NamedResults[int]() | results.MultipleResults[int]([2]),
            results.NamedResults[int]({"": 2}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.MultipleResults[int](),
            results.NamedResults[int]({"a": 1}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.MultipleResults[int]([2]),
            results.NamedResults[int]({"a": 1, "": 2}),
        )

    def test_or_named(self):
        self.assertEqual(
            results.NamedResults[int]() | results.NamedResults[int](),
            results.NamedResults[int](),
        )
        self.assertEqual(
            results.NamedResults[int]() | results.NamedResults[int]({"b": 2}),
            results.NamedResults[int]({"b": 2}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.NamedResults[int](),
            results.NamedResults[int]({"a": 1}),
        )
        self.assertEqual(
            results.NamedResults[int]({"a": 1}) | results.NamedResults[int]({"b": 2}),
            results.NamedResults[int]({"a": 1, "b": 2}),
        )

    def test_convert(self) -> None:
        @dataclass(frozen=True)
        class Decl:
            name: str
            value: int

        self.assertEqual(
            (
                results.SingleResults[str]("a").named("name")
                | results.SingleResults[int](1).named("value")
            ).convert(Decl),
            results.SingleResults[Decl](Decl("a", 1)),
        )

    def test_or_type(self):
        for lhs, rhs, expected in list[
            tuple[
                results.NamedResults[int],
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
                    results.NamedResults[int](),
                    results.NoResults[str](),
                    results.NamedResults[int | str](),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.NoResults[str](),
                    results.NamedResults[int | str]({"i": 1}),
                ),
                (
                    results.NamedResults[int](),
                    results.SingleResults[str]("a"),
                    results.NamedResults[int | str]({"": "a"}),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.SingleResults[str]("a"),
                    results.NamedResults[int | str]({"i": 1, "": "a"}),
                ),
                (
                    results.NamedResults[int](),
                    results.OptionalResults[str](),
                    results.NamedResults[int | str](),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.OptionalResults[str](),
                    results.NamedResults[int | str]({"i": 1}),
                ),
                (
                    results.NamedResults[int](),
                    results.OptionalResults[str]("a"),
                    results.NamedResults[int | str]({"": "a"}),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.OptionalResults[str]("a"),
                    results.NamedResults[int | str]({"i": 1, "": "a"}),
                ),
                (
                    results.NamedResults[int](),
                    results.MultipleResults[str](),
                    results.NamedResults[int | str](),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.MultipleResults[str](),
                    results.NamedResults[int | str]({"i": 1}),
                ),
                (
                    results.NamedResults[int](),
                    results.NamedResults[str]({"a": "v"}),
                    results.NamedResults[int | str]({"a": "v"}),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.NamedResults[str]({"a": "v"}),
                    results.NamedResults[int | str]({"i": 1, "a": "v"}),
                ),
                (
                    results.NamedResults[int](),
                    results.NamedResults[str](),
                    results.NamedResults[int | str](),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.NamedResults[str](),
                    results.NamedResults[int | str]({"i": 1}),
                ),
                (
                    results.NamedResults[int]({"i": 1}),
                    results.NamedResults[str]({"a": "v"}),
                    results.NamedResults[int | str]({"i": 1, "a": "v"}),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
