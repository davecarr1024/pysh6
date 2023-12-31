from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import expr
from pysh.pype.vals import scope
from pysh.pype.statements import result, statement


@dataclass(frozen=True)
class ExprStatement(statement.Statement):
    value: expr.Expr

    def eval(self, scope: scope.Scope) -> result.Result:
        self.value.eval(scope)
        return result.Result()

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "ExprStatement"]:
        return (expr.Expr.ref() & ";").convert(ExprStatement)
