from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import expr
from pysh.pype.vals import arg, scope


@dataclass(frozen=True)
class Arg:
    val: expr.Expr

    def __str__(self) -> str:
        return str(self.val)

    def eval(self, scope: scope.Scope) -> arg.Arg:
        return arg.Arg(self.val.eval(scope))

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Arg"]:
        return expr.Expr.ref().convert(Arg)
