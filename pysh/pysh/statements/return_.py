from dataclasses import dataclass
from typing import Optional
from pysh import core
from pysh.pysh import parser, state
from pysh.pysh.exprs import expr
from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Return(statement.Statement):
    value: Optional[expr.Expr] = None

    def _str_line(self) -> str:
        return f"return {self.value};" if self.value is not None else "return;"

    def eval(self, state: state.State) -> result.Result:
        return result.Result.for_return(
            self.value.eval(state) if self.value is not None else None
        )

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Return"]:
        return ("return" & expr.Expr.ref().zero_or_one() & ";").convert(Return)
