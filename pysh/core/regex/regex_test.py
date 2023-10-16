from typing import Optional
from unittest import TestCase
from .. import chars, errors
from ..regex import *


class RegexTest(TestCase):
    def test_apply(self):
        for regex, state, expected in list[
            tuple[Regex, chars.Stream | str, Optional[Result | str]]
        ]([]):
            if isinstance(state, str):
                state = chars.Stream.load(state)
            with self.subTest(regex=regex, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        regex(state)
                else:
                    if isinstance(expected, str):
                        expected = Result.load(expected)
                    self.assertEqual(regex(state), expected)
