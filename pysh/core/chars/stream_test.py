from typing import Optional
from unittest import TestCase

from pysh.core.chars import char, position, stream


class StreamTest(TestCase):
    def test_load(self):
        for value, position_, expected in list[
            tuple[str, Optional[position.Position], stream.Stream]
        ](
            [
                (
                    "",
                    None,
                    stream.Stream(),
                ),
                (
                    "a",
                    None,
                    stream.Stream(
                        [
                            char.Char("a"),
                        ]
                    ),
                ),
                (
                    "ab",
                    None,
                    stream.Stream(
                        [
                            char.Char("a"),
                            char.Char("b", position.Position(0, 1)),
                        ]
                    ),
                ),
                (
                    "\na",
                    None,
                    stream.Stream(
                        [
                            char.Char("\n"),
                            char.Char("a", position.Position(1, 0)),
                        ]
                    ),
                ),
                (
                    "a\n",
                    None,
                    stream.Stream(
                        [
                            char.Char("a"),
                            char.Char("\n", position.Position(0, 1)),
                        ]
                    ),
                ),
                (
                    "ab",
                    position.Position(1, 0),
                    stream.Stream(
                        [
                            char.Char("a", position.Position(1, 0)),
                            char.Char("b", position.Position(1, 1)),
                        ]
                    ),
                ),
            ]
        ):
            with self.subTest(value=value, position=position_, expected=expected):
                self.assertEqual(stream.Stream.load(value, position_), expected)
