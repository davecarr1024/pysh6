from typing import Optional
from unittest import TestCase
from . import chars, errors

class PositionTest(TestCase):
    def test_add(self):
        for pos, char, expected in list[tuple[chars.Position,chars.Char,chars.Position]]([
            (
                chars.Position(),
                chars.Char('a'),
                chars.Position(0,1),
            ),
            (
                chars.Position(),
                chars.Char('\n'),
                chars.Position(1,0),
            ),
            (
                chars.Position(1,0),
                chars.Char('a'),
                chars.Position(1,1),
            ),
        ]):
            with self.subTest(pos=pos,char=char,expected=expected):
                self.assertEqual(pos + char,expected)

class CharTest(TestCase):
    def test_ctor(self):
        for value, expected in list[tuple[str,Optional[chars.Char]]]([
            (
                '',
                None,
            ),
            (
                'a',
                chars.Char('a'),
            ),
            (
                'ab',
                None,
            ),
        ]):
            with self.subTest(value=value,expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        chars.Char(value)
                else:
                    self.assertEqual(chars.Char(value),expected)

class StreamTest(TestCase):
    def test_load(self):
        for value, position, expected in list[tuple[str,Optional[chars.Position],chars.Stream]]([
            (
                '',
                None,
                chars.Stream(),
            ),
            (
                'a',
                None,
                chars.Stream([
                    chars.Char('a'),
                ]),
            ),
            (
                'ab',
                None,
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('b',chars.Position(0,1)),
                ]),
            ),
            (
                '\na',
                None,
                chars.Stream([
                    chars.Char('\n'),
                    chars.Char('a',chars.Position(1,0)),
                ]),
            ),
            (
                'a\n',
                None,
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('\n',chars.Position(0,1)),
                ]),
            ),
            (
                'ab',
                chars.Position(1,0),
                chars.Stream([
                    chars.Char('a',chars.Position(1,0)),
                    chars.Char('b',chars.Position(1,1)),
                ]),
            ),
        ]):
            with self.subTest(value=value,position=position,expected=expected):
                self.assertEqual(chars.Stream.load(value,position),expected)
