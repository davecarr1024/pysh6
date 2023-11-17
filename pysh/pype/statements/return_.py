from dataclasses import dataclass
from typing import Optional
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import expr
from pysh.pype.vals import builtins, scope
from pysh.pype.statements import result, statement


@dataclass(frozen=True)
class Return(statement.Statement):
    value: Optional[expr.Expr] = None

    def __str__(self) -> str:
        return f"return {self.value};"

    def eval(self, scope: scope.Scope) -> result.Result:
        return result.Result.for_return(
            self.value.eval(scope) if self.value is not None else builtins.none
        )

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Return"]:
        return ("return" & expr.Expr.ref() & ";").convert(Return)
