from typing import Optional
from unittest import TestCase

from pysh import pype


class BlockTest(TestCase):
    def test_eval(self) -> None:
        for block, scope, expected in list[
            tuple[
                pype.statements.Block,
                Optional[pype.vals.Scope],
                pype.statements.Result,
            ]
        ](
            [
                (
                    pype.statements.Block(),
                    None,
                    pype.statements.Result(),
                ),
                (
                    pype.statements.Block(
                        [
                            pype.statements.ExprStatement(
                                pype.exprs.ref(pype.vals.int_(1)),
                            )
                        ]
                    ),
                    None,
                    pype.statements.Result(),
                ),
                (
                    pype.statements.Block(
                        [
                            pype.statements.Return(
                                pype.exprs.ref(pype.vals.int_(1)),
                            )
                        ]
                    ),
                    None,
                    pype.statements.Result(pype.vals.int_(1)),
                ),
                (
                    pype.statements.Block(
                        [
                            pype.statements.ExprStatement(
                                pype.exprs.ref("a"),
                            )
                        ]
                    ),
                    pype.vals.Scope({"a": pype.vals.int_(1)}),
                    pype.statements.Result(),
                ),
                (
                    pype.statements.Block(
                        [
                            pype.statements.Return(
                                pype.exprs.ref("a"),
                            )
                        ]
                    ),
                    pype.vals.Scope({"a": pype.vals.int_(1)}),
                    pype.statements.Result(pype.vals.int_(1)),
                ),
                (
                    pype.statements.Block(
                        [
                            pype.statements.Assignment(
                                pype.exprs.ref("a"),
                                pype.exprs.literal(pype.vals.int_(2)),
                            ),
                            pype.statements.Return(
                                pype.exprs.ref("a"),
                            ),
                        ]
                    ),
                    pype.vals.Scope({"a": pype.vals.int_(1)}),
                    pype.statements.Result(pype.vals.int_(2)),
                ),
            ]
        ):
            with self.subTest(block=block, scope=scope, expected=expected):
                self.assertEqual(block.eval(scope or pype.vals.Scope()), expected)
