from unittest import TestCase
from pysh.core import regex


class RegexTest(TestCase):
    def test_load(self):
        for value, expected in list[tuple[str, regex.Regex]](
            [
                (
                    "a",
                    regex.Literal("a"),
                ),
                (
                    "",
                    regex.And([]),
                ),
                (
                    "ab",
                    regex.And([regex.Literal("a"), regex.Literal("b")]),
                ),
                (
                    r"\a",
                    regex.Literal("a"),
                ),
                (
                    r"\d",
                    regex.Regex.digits(),
                ),
                (
                    r"\s",
                    regex.Regex.whitespace(),
                ),
            ]
        ):
            with self.subTest(value=value, expected=expected):
                actual = regex.Regex.load(value)
                self.assertEqual(
                    actual,
                    expected,
                    f"actual {actual} != expected {expected}",
                )
