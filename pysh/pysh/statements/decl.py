from dataclasses import dataclass
from typing import cast
from pysh import core
from pysh.pysh import parser, state
from pysh.pysh.vals import type as type_lib, var
from pysh.pysh.exprs import expr, ref
from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Decl(statement.Statement):
    type: ref.Ref
    name: str
    rhs: expr.Expr

    def _str_line(self) -> str:
        return f"{self.name}: {self.type} = {self.rhs};"

    def eval(self, state: state.State) -> result.Result:
        if not isinstance(
            type_ := cast(type_lib.Type, self.type.eval(state)),
            type_lib.Type,
        ):
            raise self._error(msg=f"decl has non-type type {self.type} = {type_}")
        if self.name in state:
            raise self._error(msg=f"duplicate var {self.name} in {repr(state)}")
        rhs = self._try(lambda: self.rhs.eval(state), msg="eval rhs")
        state[self.name] = var.Var(type_, rhs)
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Decl"]:
        return (
            ref.Ref.ref().named("lhs")
            & ":"
            & ref.Ref.ref().named("type")
            & "="
            & expr.Expr.ref().named("rhs")
            & ";"
        ).convert(Decl)
