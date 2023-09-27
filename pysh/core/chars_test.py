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
    def test_bool(self):
        for stream, expected in list[tuple[chars.Stream,bool]]([
            (
                chars.Stream(),
                False,
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                ]),
                True,
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                self.assertEqual(bool(stream),expected)

    def test_len(self):
        for stream, expected in list[tuple[chars.Stream,int]]([
            (
                chars.Stream(),
                0,
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                ]),
                1,
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('b'),
                ]),
                2,
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                self.assertEqual(len(stream),expected)

    def test_head(self):
        for stream, expected in list[tuple[chars.Stream,Optional[chars.Char]]]([
            (
                chars.Stream(),
                None,
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                ]),
                chars.Char('a'),
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('b'),
                ]),
                chars.Char('a'),
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        stream.head()
                else:
                    self.assertEqual(stream.head(),expected)

    def test_tail(self):
        for stream, expected in list[tuple[chars.Stream,Optional[chars.Stream]]]([
            (
                chars.Stream(),
                None,
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                ]),
                chars.Stream(),
            ),
            (
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('b'),
                ]),
                chars.Stream([
                    chars.Char('b'),
                ]),
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        stream.tail()
                else:
                    self.assertEqual(stream.tail(),expected)                    

    def test_load(self):
        for value, expected in list[tuple[str,chars.Stream]]([
            (
                '',
                chars.Stream(),
            ),
            (
                'a',
                chars.Stream([
                    chars.Char('a'),
                ]),
            ),
            (
                'ab',
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('b',chars.Position(0,1)),
                ]),
            ),
            (
                '\na',
                chars.Stream([
                    chars.Char('\n'),
                    chars.Char('a',chars.Position(1,0)),
                ]),
            ),
            (
                'a\n',
                chars.Stream([
                    chars.Char('a'),
                    chars.Char('\n',chars.Position(0,1)),
                ]),
            ),
        ]):
            with self.subTest(value=value,expected=expected):
                self.assertEqual(chars.Stream.load(value),expected)