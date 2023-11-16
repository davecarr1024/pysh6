from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import expr
from pysh.pype.exprs.ref import ref
from pysh.pype.statements import statement
from pysh.pype.vals import scope


@dataclass(frozen=True)
class Assignment(statement.Statement):
    lhs: ref.Ref
    rhs: expr.Expr

    def __str__(self) -> str:
        return f"{self.lhs} = {self.rhs};"

    def eval(self, scope: scope.Scope) -> None:
        self.lhs.set(scope, self.rhs.eval(scope))

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Assignment"]:
        return (
            ref.Ref.ref().named("lhs") & "=" & expr.Expr.ref().named("rhs") & ";"
        ).convert(Assignment)
