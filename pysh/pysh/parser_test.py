from typing import Optional
from unittest import TestCase

from pysh import core, pysh


class ParserTest(TestCase):
    def test_eval(self) -> None:
        for input, state, expected in list[
            tuple[
                str,
                Optional[pysh.State],
                Optional[pysh.vals.Val],
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
                    pysh.vals.none,
                ),
                (
                    "return 1;",
                    None,
                    pysh.vals.int_(1),
                ),
                (
                    "return a;",
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(pysh.vals.int_(1)),
                            }
                        )
                    ),
                    pysh.vals.int_(1),
                ),
                (
                    "a: int = 1; return a;",
                    None,
                    pysh.vals.int_(1),
                ),
                (
                    "a: int; a: int;",
                    None,
                    None,
                ),
                (
                    "a: int; return a;",
                    None,
                    None,
                ),
                (
                    "a: int; a = 1; return a;",
                    None,
                    pysh.vals.int_(1),
                ),
                (
                    "def f() -> int { return 1; } return f();",
                    None,
                    pysh.vals.int_(1),
                ),
                (
                    "def f() -> int { return a; } return f();",
                    pysh.State().as_child(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.int_(1),
                                )
                            }
                        )
                    ),
                    pysh.vals.int_(1),
                ),
                (
                    "def f(a: int) -> int { return a; } return f(1);",
                    None,
                    pysh.vals.int_(1),
                ),
                (
                    "def f(a: int, b: int) -> int { return a; } return f(1, 2);",
                    None,
                    pysh.vals.int_(1),
                ),
            ]
        ):
            with self.subTest(
                input=input,
                state=str(state),
                expected=str(expected),
            ):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pysh.Parser.eval(input, state)
                else:
                    actual = pysh.Parser.eval(input, state)
                    self.assertEqual(
                        actual,
                        expected,
                        f"actual {actual} != expected {expected}",
                    )
