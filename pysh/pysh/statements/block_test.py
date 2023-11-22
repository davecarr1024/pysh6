from unittest import TestCase
from pysh import pysh


class BlockTest(TestCase):
    def test_eval(self) -> None:
        for block, state, expected in list[
            tuple[
                pysh.statements.Block,
                pysh.State,
                pysh.statements.Result,
            ]
        ](
            [
                (
                    pysh.statements.Block(),
                    pysh.State(),
                    pysh.statements.Result(),
                ),
                (
                    pysh.statements.Block(
                        [
                            pysh.statements.Return(
                                pysh.exprs.literal(
                                    pysh.vals.int_(1),
                                )
                            )
                        ]
                    ),
                    pysh.State(),
                    pysh.statements.Result.for_return(
                        pysh.vals.int_(1),
                    ),
                ),
                (
                    pysh.statements.Block(
                        [
                            pysh.statements.Return(
                                pysh.exprs.ref_("a"),
                            ),
                        ]
                    ),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(pysh.vals.int_(1)),
                            }
                        )
                    ),
                    pysh.statements.Result.for_return(
                        pysh.vals.int_(1),
                    ),
                ),
            ]
        ):
            with self.subTest(block=block, state=state, expected=expected):
                self.assertEqual(block.eval(state), expected)
