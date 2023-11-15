from dataclasses import dataclass
from pysh import core
from pysh.pype import exprs, parser, vals
from pysh.pype.statements import statement


@dataclass(frozen=True)
class ExprStatement(statement.Statement):
    value: exprs.Expr

    def eval(self, scope: vals.Scope) -> None:
        self.value.eval(scope)

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "ExprStatement"]:
        return exprs.Expr.ref().convert(ExprStatement)
