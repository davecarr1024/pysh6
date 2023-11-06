from typing import Optional
import unittest
from pysh.core import errors
from pysh.core.streams import stream


class _IntStream(stream.Stream[int, "_IntStream"]):
    ...


class StreamTest(unittest.TestCase):
    def test_len(self):
        for stream, expected in list[tuple[_IntStream, int]](
            [
                (
                    _IntStream(),
                    0,
                ),
                (
                    _IntStream([1]),
                    1,
                ),
                (
                    _IntStream([1, 2]),
                    2,
                ),
            ]
        ):
            with self.subTest(stream=stream, expected=expected):
                self.assertEqual(len(stream), expected)

    def test_bool(self):
        for stream, expected in list[tuple[_IntStream, bool]](
            [
                (
                    _IntStream(),
                    False,
                ),
                (
                    _IntStream([1]),
                    True,
                ),
            ]
        ):
            with self.subTest(stream=stream, expected=expected):
                self.assertEqual(bool(stream), expected)

    def test_head(self):
        for stream, expected in list[tuple[_IntStream, Optional[int]]](
            [
                (
                    _IntStream(),
                    None,
                ),
                (
                    _IntStream([1]),
                    1,
                ),
                (
                    _IntStream([1, 2]),
                    1,
                ),
            ]
        ):
            with self.subTest(stream=stream, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        stream.head()
                else:
                    self.assertEqual(stream.head(), expected)

    def test_tail(self):
        for stream, expected in list[tuple[_IntStream, Optional[_IntStream]]](
            [
                (
                    _IntStream(),
                    None,
                ),
                (
                    _IntStream([1]),
                    _IntStream(),
                ),
                (
                    _IntStream([1, 2]),
                    _IntStream([2]),
                ),
            ]
        ):
            with self.subTest(stream=stream, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        stream.tail()
                else:
                    self.assertEqual(stream.tail(), expected)
