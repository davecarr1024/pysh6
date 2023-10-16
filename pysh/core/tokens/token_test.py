from typing import Optional, Sequence
from unittest import TestCase
from .. import chars, errors
from . import token


class TokenTest(TestCase):
    def test_load(self):
        for rule_name, value, expected in list[
            tuple[str, Sequence[chars.Char] | chars.Stream, Optional[token.Token]]
        ](
            [
                (
                    "r",
                    [],
                    None,
                ),
                (
                    "r",
                    [
                        chars.Char("a"),
                        chars.Char("b"),
                    ],
                    token.Token("r", "ab"),
                ),
                (
                    "r",
                    [
                        chars.Char("a", chars.Position(1, 0)),
                        chars.Char("b"),
                    ],
                    token.Token("r", "ab", chars.Position(1, 0)),
                ),
                (
                    "r",
                    chars.Stream(),
                    None,
                ),
                (
                    "r",
                    chars.Stream.load("abc"),
                    token.Token("r", "abc"),
                ),
                (
                    "r",
                    chars.Stream.load("abc", chars.Position(1, 0)),
                    token.Token("r", "abc", chars.Position(1, 0)),
                ),
            ]
        ):
            with self.subTest(rule_name=rule_name, value=value, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        token.Token.load(rule_name, value)
                else:
                    self.assertEqual(token.Token.load(rule_name, value), expected)
