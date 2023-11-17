from unittest import TestCase
from pysh import pype


class FuncTest(TestCase):
    def test_call(self) -> None:
        for func, scope, args, expected in list[
            tuple[
                pype.funcs.Func,
                pype.vals.Scope,
                pype.vals.Args,
                pype.vals.Val,
            ]
        ](
            [
                (
                    pype.funcs.Func(
                        _name="f",
                    ),
                    pype.vals.Scope(),
                    pype.vals.Args(),
                    pype.vals.none,
                ),
                (
                    pype.funcs.Func(
                        _name="f",
                        body=pype.statements.Block(
                            [
                                pype.statements.Return(
                                    pype.exprs.literal(
                                        pype.vals.int_(1),
                                    )
                                )
                            ]
                        ),
                    ),
                    pype.vals.Scope(),
                    pype.vals.Args(),
                    pype.vals.int_(1),
                ),
                (
                    pype.funcs.Func(
                        _name="f",
                        body=pype.statements.Block(
                            [
                                pype.statements.Return(
                                    pype.exprs.ref(
                                        "a",
                                    )
                                )
                            ]
                        ),
                    ),
                    pype.vals.Scope({"a": pype.vals.int_(1)}),
                    pype.vals.Args(),
                    pype.vals.int_(1),
                ),
                (
                    pype.funcs.Func(
                        _name="f",
                        body=pype.statements.Block(
                            [
                                pype.statements.Return(
                                    pype.exprs.ref(
                                        "a",
                                    )
                                )
                            ]
                        ),
                        params=pype.exprs.Params([pype.exprs.Param("a")]),
                    ),
                    pype.vals.Scope(),
                    pype.vals.Args([pype.vals.Arg(pype.vals.int_(1))]),
                    pype.vals.int_(1),
                ),
            ]
        ):
            with self.subTest((func, scope, args, expected)):
                self.assertEqual(func(scope, args), expected)
