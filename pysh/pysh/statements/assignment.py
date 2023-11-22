from dataclasses import dataclass
from pysh import core
from pysh.pysh import parser, state
from pysh.pysh.exprs import expr, ref
from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Assignment(statement.Statement):
    lhs: ref.Ref
    rhs: expr.Expr

    def __str__(self) -> str:
        return f"{self.lhs} = {self.rhs};"

    def eval(self, state: state.State) -> result.Result:
        self._try(lambda: self.lhs.set(state, self.rhs.eval(state)))
        return result.Result()

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Assignment"]:
        return (
            ref.Ref.ref().named("lhs") & "=" & expr.Expr.ref().named("rhs") & ";"
        ).convert(Assignment)
