from typing import Mapping
from unittest import TestCase
from .. import regex
from . import lexer, rule


class LexerTest(TestCase):
    def test_load(self):
        for regexes, expected in list[
            tuple[Mapping[str, str | regex.Regex], lexer.Lexer]
        ](
            [
                (
                    {},
                    lexer.Lexer(),
                ),
                (
                    {
                        "a": "a",
                    },
                    lexer.Lexer([rule.Rule.load("a")]),
                ),
                (
                    {
                        "r": "a",
                    },
                    lexer.Lexer([rule.Rule.load("r", "a")]),
                ),
            ]
        ):
            with self.subTest(regexes=regexes, expected=expected):
                self.assertEqual(lexer.Lexer.load(**regexes), expected)
