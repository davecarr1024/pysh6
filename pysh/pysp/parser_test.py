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
                    " 1 ",
                    pysp.Int(1),
                ),
                (
                    '"a"',
                    pysp.Str("a"),
                ),
                (
                    ' "a" ',
                    pysp.Str("a"),
                ),
                (
                    '" a "',
                    pysp.Str(" a "),
                ),
                (
                    '"',
                    None,
                ),
                (
                    r"( lambda () 1 )",
                    pysp.Func([], pysp.Literal(pysp.Int(1))),
                ),
                (
                    r"(def a 1) a",
                    pysp.Int(1),
                ),
                (
                    r"(def a (lambda () 1)) (a)",
                    pysp.Int(1),
                ),
                (
                    r"(def a (lambda (b) b)) (a 1)",
                    pysp.Int(1),
                ),
                (
                    r"(def a (lambda (a) a)) (a 1)",
                    pysp.Int(1),
                ),
            ]
        ):
            with self.subTest(input=input, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pysp.Parser.eval(input)
                else:
                    self.assertEqual(pysp.Parser.eval(input), expected)
