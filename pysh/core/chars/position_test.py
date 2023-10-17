from unittest import TestCase
from pysh.core.chars import char, position


class PositionTest(TestCase):
    def test_add(self):
        for pos, char_, expected in list[
            tuple[position.Position, char.Char, position.Position]
        ](
            [
                (
                    position.Position(),
                    char.Char("a"),
                    position.Position(0, 1),
                ),
                (
                    position.Position(),
                    char.Char("\n"),
                    position.Position(1, 0),
                ),
                (
                    position.Position(1, 0),
                    char.Char("a"),
                    position.Position(1, 1),
                ),
            ]
        ):
            with self.subTest(pos=pos, char=char_, expected=expected):
                self.assertEqual(pos + char_, expected)
