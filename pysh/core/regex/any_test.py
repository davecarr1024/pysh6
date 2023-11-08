from unittest import TestCase
from pysh.core import chars, errors, regex


class AnyTest(TestCase):
    def test_call(self):
        with self.assertRaises(errors.Error):
            regex.Any()(regex.State())
        self.assertEqual(
            regex.Any()(regex.State.load("a")),
            regex.State().and_result(regex.Result.load("a")),
        )
        self.assertEqual(
            regex.Any()(regex.State.load("ab")),
            regex.State.load("b", chars.Position(0, 1)).and_result(
                regex.Result.load("a")
            ),
        )
