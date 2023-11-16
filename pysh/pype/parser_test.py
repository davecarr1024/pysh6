from typing import Optional
from unittest import TestCase

from pysh import core, pype


class ParserTest(TestCase):
    def test_eval(self) -> None:
        for input, scope, expected in list[
            tuple[
                str,
                Optional[pype.vals.Scope],
                Optional[pype.vals.Val],
            ]
        ](
            [
                (
                    "",
                    None,
                    None,
                ),
                (
                    "1;",
                    None,
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    "a;",
                    None,
                    None,
                ),
                (
                    "a;",
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    "a.b;",
                    pype.vals.Scope(
                        {
                            "a": pype.vals.classes.Object(
                                class_=pype.vals.classes.Class(_name="c"),
                                members=pype.vals.Scope(
                                    {
                                        "b": pype.vals.builtins.Int.create(1),
                                    }
                                ),
                            )
                        }
                    ),
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    "class c {}; c;",
                    None,
                    pype.vals.classes.Class(_name="c"),
                ),
                (
                    "a = 1; a;",
                    None,
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    r"""
                        class c {};
                        c.a = 1;
                        c.a;
                    """,
                    None,
                    pype.vals.builtins.Int.create(1),
                ),
            ]
        ):
            with self.subTest(input=input, scope=scope, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pype.Parser.eval(input, scope)
                else:
                    self.assertEqual(pype.Parser.eval(input, scope), expected)
