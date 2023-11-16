from typing import Optional
from unittest import TestCase

from pysh import core, pype


class ParserTest(TestCase):
    def test_eval(self) -> None:
        for input, expected in list[
            tuple[
                str,
                Optional[pype.vals.Val],
            ]
        ](
            [
                (
                    "",
                    None,
                ),
                (
                    "1;",
                    pype.vals.builtins.Int.create(1),
                ),
            ]
        ):
            with self.subTest(input=input, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pype.Parser.eval(input)
                else:
                    self.assertEqual(pype.Parser.eval(input), expected)
