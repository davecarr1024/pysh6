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

    def test_convert(self):
        self.assertEqual(
            results.NoResult[int]().convert(lambda _: results.SingleResult[int](0)),
            results.SingleResult[int](0),
        )
