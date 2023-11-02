from unittest import TestCase
from pysh.core.parser import results


class NoResultTest(TestCase):
    def test_no(self):
        self.assertEqual(results.NoResult[int]().no(), results.NoResult[int]())

    def test_single(self):
        with self.assertRaises(results.Error):
            results.NoResult[int]().single()

    def test_optional(self):
        self.assertEqual(
            results.NoResult[int]().optional(), results.OptionalResult[int]()
        )

    def test_multiple(self):
        self.assertEqual(
            results.NoResult[int]().multiple(), results.MultipleResult[int]()
        )

    def test_named(self):
        self.assertEqual(results.NoResult[int]().named("a"), results.NamedResult[int]())

    def test_convert(self) -> None:
        def convert() -> int:
            return 0

        self.assertEqual(
            results.NoResult[int]().convert_type(convert),
            results.SingleResult[int](0),
        )

    def test_or(self):
        for lhs, rhs, expected in list[
            tuple[results.NoResult[int], results.OrArgs, results.Results[int]]
        ](
            [
                (
                    results.NoResult[int](),
                    results.NoResult[int](),
                    results.NoResult[int](),
                ),
                (
                    results.NoResult[int](),
                    results.SingleResult[int](0),
                    results.SingleResult[int](0),
                ),
                (
                    results.NoResult[int](),
                    results.OptionalResult[int](0),
                    results.OptionalResult[int](0),
                ),
                (
                    results.NoResult[int](),
                    results.MultipleResult[int]([0]),
                    results.MultipleResult[int]([0]),
                ),
                (
                    results.NoResult[int](),
                    results.NamedResult[int]({"a": 0}),
                    results.NamedResult[int]({"a": 0}),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
