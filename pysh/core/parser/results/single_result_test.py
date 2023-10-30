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
        self.assertEqual(
            results.SingleResult[int](1).convert(
                lambda r: results.SingleResult[int](r.result * 2)
            ),
            results.SingleResult[int](2),
        )
