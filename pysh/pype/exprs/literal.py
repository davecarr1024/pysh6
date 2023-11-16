from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val
from pysh.pype.exprs import expr


@dataclass(frozen=True)
class Literal(expr.Expr):
    val_: val.Val

    def eval(self, scope: scope.Scope) -> val.Val:
        return self.val_

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Literal"]:
        return val.Val.ref().convert(Literal)
