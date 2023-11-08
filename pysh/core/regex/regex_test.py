from unittest import TestCase
from pysh.core.regex import and_, literal, regex


class RegexTest(TestCase):
    def test_load(self):
        self.assertEqual(regex.Regex.load(""), and_.And([]))
        self.assertEqual(regex.Regex.load("a"), literal.Literal("a"))
        self.assertEqual(
            regex.Regex.load("ab"),
            and_.And([literal.Literal("a"), literal.Literal("b")]),
        )
