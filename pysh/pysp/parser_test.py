from typing import Optional
from unittest import TestCase

from pysh import core, pysp


class ParserTest(TestCase):
    def test_eval(self):
        for input, expected in list[
            tuple[
                str,
                Optional[pysp.Val],
            ]
        ](
            [
                (
                    "",
                    None,
                ),
                (
                    "1",
                    pysp.Int(1),
                ),
                (
                    '"a"',
                    pysp.Str("a"),
                ),
                (
                    '"',
                    None,
                ),
            ]
        ):
            with self.subTest(input=input, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pysp.Parser.eval(input)
                else:
                    self.assertEqual(pysp.Parser.eval(input), expected)
