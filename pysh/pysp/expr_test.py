from typing import Optional
from unittest import TestCase
from pysh import core, pysp


class ExprTest(TestCase):
    def test_load(self) -> None:
        for state, expected in list[
            tuple[
                pysp.Parser,
                Optional[
                    core.parser.states.StateAndSingleResults[pysp.Parser, pysp.Expr]
                ],
            ]
        ](
            [
                (
                    pysp.Parser(),
                    None,
                ),
                (
                    pysp.Parser.load(core.tokens.Token("int", "1")),
                    core.parser.states.StateAndSingleResults[pysp.Parser, pysp.Expr](
                        pysp.Parser(),
                        core.parser.results.SingleResults[pysp.Expr](
                            pysp.Literal(pysp.Int(1))
                        ),
                    ),
                ),
                (
                    pysp.Parser.load(core.tokens.Token("str", '"a"')),
                    core.parser.states.StateAndSingleResults[pysp.Parser, pysp.Expr](
                        pysp.Parser(),
                        core.parser.results.SingleResults[pysp.Expr](
                            pysp.Literal(pysp.Str("a"))
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        pysp.Expr.ref()(state)
                else:
                    self.assertEqual(pysp.Expr.ref()(state), expected)
