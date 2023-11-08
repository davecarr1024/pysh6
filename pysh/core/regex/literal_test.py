from unittest import TestCase
from pysh.core import chars, errors, regex


class LiteralTest(TestCase):
    def test_ctor_empty(self):
        with self.assertRaises(errors.Error):
            regex.Literal("")

    def test_ctor_too_many(self):
        with self.assertRaises(errors.Error):
            regex.Literal("ab")

    def test_call_empty(self):
        with self.assertRaises(errors.Error):
            regex.Literal("a")(regex.State())

    def test_call_mismatch(self):
        with self.assertRaises(errors.Error):
            regex.Literal("a")(regex.State.load("b"))

    def test_call_match(self):
        self.assertEqual(
            regex.Literal("a")(regex.State.load("a")),
            regex.State().and_result(regex.Result.load("a")),
        )

    def test_call_match_extra(self):
        self.assertEqual(
            regex.Literal("a")(regex.State.load("ab")),
            regex.State.load("b", chars.Position(0, 1)).and_result(
                regex.Result.load("a")
            ),
        )
