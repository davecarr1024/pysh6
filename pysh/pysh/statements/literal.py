from dataclasses import dataclass
from pysh import core
from pysh.pysh import parser, state
from pysh.pysh.exprs import expr
from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Literal(statement.Statement):
    val: expr.Expr

    def __str__(self) -> str:
        return f"{self.val};"

    def eval(self, state: state.State) -> result.Result:
        self._try(lambda: self.val.eval(state), "evaluate literal statement")
        return result.Result()

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Literal"]:
        return (expr.Expr.ref() & ";").convert(Literal)
