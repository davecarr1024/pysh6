from dataclasses import dataclass
from pysh import core
from pysh.pype import parser, vals
from pysh.pype.exprs import expr


@dataclass(frozen=True)
class Literal(expr.Expr):
    val: vals.Val

    def eval(self, scope: vals.Scope) -> vals.Val:
        return self.val

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Literal"]:
        return vals.Val.ref().convert(Literal)
