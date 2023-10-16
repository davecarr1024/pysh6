from typing import Optional
from unittest import TestCase
from . import char
from .. import errors


class CharTest(TestCase):
    def test_ctor(self):
        for value, expected in list[tuple[str, Optional[char.Char]]](
            [
                (
                    "",
                    None,
                ),
                (
                    "a",
                    char.Char("a"),
                ),
                (
                    "ab",
                    None,
                ),
            ]
        ):
            with self.subTest(value=value, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        char.Char(value)
                else:
                    self.assertEqual(char.Char(value), expected)
