from typing import Optional
from unittest import TestCase

from pyparsing import str_type
from pysh.core import errors
from pysh.core.parser import results


class NamedResultTest(TestCase):
    def test_no(self):
        for result, expected in list[
            tuple[results.NamedResult[int], results.NoResult[int]]
        ](
            [
                (results.NamedResult[int](), results.NoResult[int]()),
                (results.NamedResult[int]({"a": 1}), results.NoResult[int]()),
                (results.NamedResult[int]({"a": 1, "b": 2}), results.NoResult[int]()),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                self.assertEqual(result.no(), expected)

    def test_single(self):
        for result, expected in list[
            tuple[results.NamedResult[int], Optional[results.SingleResult[int]]]
        ](
            [
                (results.NamedResult[int](), None),
                (results.NamedResult[int]({"a": 1}), results.SingleResult[int](1)),
                (results.NamedResult[int]({"a": 1, "b": 2}), None),
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
            tuple[results.NamedResult[int], Optional[results.OptionalResult[int]]]
        ](
            [
                (results.NamedResult[int](), results.OptionalResult[int]()),
                (results.NamedResult[int]({"a": 1}), results.OptionalResult[int](1)),
                (
                    results.NamedResult[int]({"a": 1, "b": 2}),
                    results.OptionalResult[int](1),
                ),
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
            tuple[results.NamedResult[int], Optional[results.MultipleResult[int]]]
        ](
            [
                (results.NamedResult[int](), results.MultipleResult[int]()),
                (
                    results.NamedResult[int]({"a": 1}),
                    results.MultipleResult[int]([1]),
                ),
                (
                    results.NamedResult[int]({"a": 1, "b": 2}),
                    results.MultipleResult[int]([1, 2]),
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
            tuple[results.NamedResult[int], Optional[results.NamedResult[int]]]
        ](
            [
                (results.NamedResult[int](), results.NamedResult[int]()),
                (
                    results.NamedResult[int]({"a": 1}),
                    results.NamedResult[int]({"a": 1}),
                ),
                (
                    results.NamedResult[int]({"a": 1, "b": 2}),
                    results.NamedResult[int]({"a": 1, "b": 2}),
                ),
            ]
        ):
            with self.subTest(results=result, expected=expected):
                if expected is None:
                    with self.assertRaises(results.Error):
                        result.named("a")
                else:
                    self.assertEqual(result.named("a"), expected)

    def test_convert_type(self):
        for result, expected in list[
            tuple[results.NamedResult[str], Optional[results.SingleResult[int]]]
        ](
            [
                (
                    results.NamedResult[str](),
                    None,
                ),
                (
                    results.NamedResult[str]({"a": "1"}),
                    None,
                ),
                (
                    results.NamedResult[str]({"b": "2"}),
                    None,
                ),
                (
                    results.NamedResult[str]({"a": "1", "b": "2"}),
                    results.SingleResult[int](12),
                ),
                (
                    results.NamedResult[str]({"a": "1", "b": "2", "c": "3"}),
                    None,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):

                def convert_type(a: str, b: str) -> int:
                    return int(a) * 10 + int(b)

                if expected is None:
                    with self.assertRaises(errors.Error):
                        result.convert_type(convert_type)
                else:
                    self.assertEqual(result.convert_type(convert_type), expected)

    def test_convert(self):
        for result, expected in list[
            tuple[results.NamedResult[int], Optional[results.SingleResult[int]]]
        ](
            [
                (
                    results.NamedResult[int](),
                    None,
                ),
                (
                    results.NamedResult[int]({"a": 1}),
                    None,
                ),
                (
                    results.NamedResult[int]({"b": 2}),
                    None,
                ),
                (
                    results.NamedResult[int]({"a": 1, "b": 2}),
                    results.SingleResult[int](12),
                ),
                (
                    results.NamedResult[int]({"a": 1, "b": 2, "c": 3}),
                    None,
                ),
            ]
        ):
            with self.subTest(result=result, expected=expected):

                def convert(a: int, b: int) -> int:
                    return a * 10 + b

                if expected is None:
                    with self.assertRaises(errors.Error):
                        result.convert(convert)
                else:
                    self.assertEqual(result.convert(convert), expected)

    def test_or(self):
        for lhs, rhs, expected in list[
            tuple[results.NamedResult[int], results.OrArgs, results.Results[int]]
        ](
            [
                (
                    results.NamedResult[int](),
                    results.NoResult[int](),
                    results.NamedResult[int](),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.NoResult[int](),
                    results.NamedResult[int]({"a": 0}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.NoResult[int](),
                    results.NamedResult[int]({"a": 0, "b": 1}),
                ),
                (
                    results.NamedResult[int](),
                    results.SingleResult[int](2),
                    results.NamedResult[int]({"": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.SingleResult[int](2),
                    results.NamedResult[int]({"a": 0, "": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.SingleResult[int](2),
                    results.NamedResult[int]({"a": 0, "b": 1, "": 2}),
                ),
                (
                    results.NamedResult[int](),
                    results.OptionalResult[int](),
                    results.NamedResult[int](),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.OptionalResult[int](),
                    results.NamedResult[int]({"a": 0}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.OptionalResult[int](),
                    results.NamedResult[int]({"a": 0, "b": 1}),
                ),
                (
                    results.NamedResult[int](),
                    results.OptionalResult[int](2),
                    results.NamedResult[int]({"": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.OptionalResult[int](2),
                    results.NamedResult[int]({"a": 0, "": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.OptionalResult[int](2),
                    results.NamedResult[int]({"a": 0, "b": 1, "": 2}),
                ),
                (
                    results.NamedResult[int](),
                    results.NamedResult[int](),
                    results.NamedResult[int](),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.NamedResult[int](),
                    results.NamedResult[int]({"a": 0}),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.MultipleResult[int]([2]),
                    results.NamedResult[int]({"a": 0, "": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.MultipleResult[int]([2, 3]),
                    results.NamedResult[int]({"a": 0, "": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.NamedResult[int](),
                    results.NamedResult[int]({"a": 0, "b": 1}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.MultipleResult[int]([2]),
                    results.NamedResult[int]({"a": 0, "b": 1, "": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.MultipleResult[int]([2, 3]),
                    results.NamedResult[int]({"a": 0, "b": 1, "": 2}),
                ),
                (
                    results.NamedResult[int](),
                    results.NamedResult[int]({"a": 2}),
                    results.NamedResult[int]({"a": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0}),
                    results.NamedResult[int]({"c": 2}),
                    results.NamedResult[int]({"a": 0, "c": 2}),
                ),
                (
                    results.NamedResult[int]({"a": 0, "b": 1}),
                    results.NamedResult[int]({"c": 2}),
                    results.NamedResult[int]({"a": 0, "b": 1, "c": 2}),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
