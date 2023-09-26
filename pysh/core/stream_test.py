from typing import Optional
import unittest
from . import errors, stream

IntStream = stream.Stream[int]

class StreamTest(unittest.TestCase):
    def test_len(self):
        for stream, expected in list[tuple[IntStream,int]]([
            (
                IntStream(),
                0,
            ),
            (
                IntStream([1]),
                1,
            ),
            (
                IntStream([1,2]),
                2,
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                self.assertEqual(len(stream),expected)

    def test_bool(self):
        for stream, expected in list[tuple[IntStream,bool]]([
            (
                IntStream(),
                False,
            ),
            (
                IntStream([1]),
                True,
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                self.assertEqual(bool(stream),expected)

    def test_head(self):
        for stream, expected in list[tuple[IntStream,Optional[int]]]([
            (
                IntStream(),
                None,
            ),
            (
                IntStream([1]),
                1,
            ),
            (
                IntStream([1,2]),
                1,
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        stream.head()
                else:
                    self.assertEqual(stream.head(),expected)

    def test_tail(self):
        for stream, expected in list[tuple[IntStream,Optional[IntStream]]]([
            (
                IntStream(),
                None,
            ),
            (
                IntStream([1]),
                IntStream(),
            ),
            (
                IntStream([1,2]),
                IntStream([2]),
            ),
        ]):
            with self.subTest(stream=stream,expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        stream.tail()
                else:
                    self.assertEqual(stream.tail(),expected)