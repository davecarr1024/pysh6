from typing import Optional
from unittest import TestCase
from pysh import core, pysh


class AssignmentTest(TestCase):
    def test_eval(self) -> None:
        for assignment, state, expected in list[
            tuple[
                pysh.statements.Assignment,
                pysh.State,
                Optional[pysh.State],
            ]
        ](
            [
                (
                    pysh.statements.Assignment(
                        pysh.exprs.ref_("a"),
                        pysh.exprs.literal(
                            pysh.vals.int_(1),
                        ),
                    ),
                    pysh.State(),
                    None,
                ),
                (
                    pysh.statements.Assignment(
                        pysh.exprs.ref_("a"),
                        pysh.exprs.literal(
                            pysh.vals.int_(1),
                        ),
                    ),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var(
                                    pysh.vals.int_class,
                                ),
                            }
                        )
                    ),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.int_(1),
                                )
                            }
                        )
                    ),
                ),
            ]
        ):
            with self.subTest(assignment=assignment, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        assignment.eval(state)
                else:
                    assignment.eval(state)
                    self.assertEqual(
                        state,
                        expected,
                        f"actual {state} != expected {expected}",
                    )
