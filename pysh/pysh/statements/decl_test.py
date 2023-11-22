from typing import Optional
from unittest import TestCase
from pysh import core, pysh


class DeclTest(TestCase):
    def test_eval(self) -> None:
        for decl, state, expected in list[
            tuple[
                pysh.statements.Decl,
                pysh.State,
                Optional[pysh.State],
            ]
        ](
            [
                (
                    pysh.statements.Decl(
                        pysh.exprs.literal(pysh.vals.int_(1)),
                        "a",
                        pysh.exprs.literal(pysh.vals.int_(1)),
                    ),
                    pysh.State(),
                    None,
                ),
                (
                    pysh.statements.Decl(
                        pysh.exprs.literal(
                            pysh.vals.int_class,
                        ),
                        "a",
                        pysh.exprs.literal(
                            pysh.vals.none,
                        ),
                    ),
                    pysh.State(),
                    None,
                ),
                (
                    pysh.statements.Decl(
                        pysh.exprs.literal(
                            pysh.vals.int_class,
                        ),
                        "a",
                        pysh.exprs.literal(
                            pysh.vals.int_(1),
                        ),
                    ),
                    pysh.State().as_child(),
                    pysh.State().as_child(
                        {
                            "a": pysh.vals.Var.for_val(
                                pysh.vals.int_(1),
                            )
                        }
                    ),
                ),
                (
                    pysh.statements.Decl(
                        pysh.exprs.ref_("int"),
                        "a",
                        pysh.exprs.literal(
                            pysh.vals.int_(2),
                        ),
                    ),
                    pysh.State().as_child(),
                    pysh.State().as_child(
                        {
                            "a": pysh.vals.Var.for_val(
                                pysh.vals.int_(2),
                            )
                        }
                    ),
                ),
                (
                    pysh.statements.Decl(
                        pysh.exprs.ref_("int"),
                        "a",
                    ),
                    pysh.State().as_child(),
                    pysh.State().as_child(
                        {
                            "a": pysh.vals.Var(pysh.vals.int_class),
                        }
                    ),
                ),
            ]
        ):
            with self.subTest(decl=decl, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        decl.eval(state)
                else:
                    decl.eval(state)
                    self.assertEqual(
                        state,
                        expected,
                        f"actual {state} != expected {expected}",
                    )
