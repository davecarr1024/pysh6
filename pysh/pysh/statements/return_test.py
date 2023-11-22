from typing import Optional
from unittest import TestCase
from pysh import core, pysh


class ReturnTest(TestCase):
    def test_eval(self) -> None:
        for return_, state, expected in list[
            tuple[
                pysh.statements.Return,
                pysh.State,
                Optional[pysh.statements.Result],
            ]
        ](
            [
                (
                    pysh.statements.Return(),
                    pysh.State(),
                    pysh.statements.Result.for_return(),
                ),
                (
                    pysh.statements.Return(
                        pysh.exprs.literal(pysh.vals.int_(1)),
                    ),
                    pysh.State(),
                    pysh.statements.Result.for_return(
                        pysh.vals.int_(1),
                    ),
                ),
                (
                    pysh.statements.Return(
                        pysh.exprs.ref_("a"),
                    ),
                    pysh.State(),
                    None,
                ),
                (
                    pysh.statements.Return(
                        pysh.exprs.ref_("a"),
                    ),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.int_(1),
                                ),
                            }
                        )
                    ),
                    pysh.statements.Result.for_return(
                        pysh.vals.int_(1),
                    ),
                ),
            ]
        ):
            with self.subTest(return_=return_, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        return_.eval(state)
                else:
                    self.assertEqual(return_.eval(state), expected)
