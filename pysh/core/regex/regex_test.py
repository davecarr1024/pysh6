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
            ]
        ):
            with self.subTest(value=value, expected=expected):
                self.assertEqual(regex.Regex.load(value), expected)
