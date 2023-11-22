from typing import Optional
from unittest import TestCase

from pysh import core, pysh


class ParserTest(TestCase):
    def test_eval(self) -> None:
        for input, expected in list[
            tuple[
                str,
                Optional[pysh.vals.Val],
            ]
        ](
            [
                (
                    "",
                    None,
                ),
                (
                    ";",
                    pysh.vals.none,
                ),
                (
                    "return 1;",
                    pysh.vals.int_(1),
                ),
            ]
        ):
            with self.subTest(input=input, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pysh.Parser.eval(input)
                else:
                    self.assertEqual(pysh.Parser.eval(input), expected)
