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
                    ";",
                    None,
                    pype.vals.builtins.none,
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
                    "class c {} c;",
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
                        class c {}
                        c.a = 1;
                        c.a;
                    """,
                    None,
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    r"""
                    a = 1;
                    {
                        a = 2;
                    }
                    a;
                    """,
                    None,
                    pype.vals.int_(1),
                ),
                (
                    "def f() {} f;",
                    None,
                    pype.funcs.Func(name="f"),
                ),
                (
                    "def f(a) {} f;",
                    None,
                    pype.funcs.Func(
                        name="f",
                        params=pype.exprs.Params(
                            [
                                pype.exprs.Param("a"),
                            ]
                        ),
                    ),
                ),
                (
                    "def f(a, b) {} f;",
                    None,
                    pype.funcs.Func(
                        name="f",
                        params=pype.exprs.Params(
                            [
                                pype.exprs.Param("a"),
                                pype.exprs.Param("b"),
                            ]
                        ),
                    ),
                ),
                (
                    "def f() { return 1; } f;",
                    None,
                    pype.funcs.Func(
                        name="f",
                        body=pype.statements.Block(
                            [
                                pype.statements.Return(
                                    pype.exprs.literal(pype.vals.int_(1))
                                )
                            ]
                        ),
                    ),
                ),
                (
                    "def f() { return 1; } f();",
                    None,
                    pype.vals.int_(1),
                ),
                (
                    "def f(a) { return a; } f(1);",
                    None,
                    pype.vals.int_(1),
                ),
            ]
        ):
            with self.subTest(input=input, scope=scope, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pype.Parser.eval(input, scope)
                else:
                    self.assertEqual(pype.Parser.eval(input, scope), expected)
