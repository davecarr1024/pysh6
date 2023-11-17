from unittest import TestCase
from pysh import pype


class AssignmentTest(TestCase):
    def test_eval(self) -> None:
        for statement, scope_, expected in list[
            tuple[
                pype.statements.Assignment,
                pype.vals.Scope,
                pype.vals.Scope,
            ]
        ](
            [
                (
                    pype.statements.Assignment(
                        pype.exprs.refs.Ref.create("a"),
                        pype.exprs.refs.Ref.create(pype.vals.builtins.Int.create(1)),
                    ),
                    pype.vals.Scope(),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                ),
            ]
        ):
            with self.subTest((statement, scope_, expected)):
                statement.eval(scope_)
                self.assertEqual(scope_, expected)
