from dataclasses import dataclass
from typing import cast
from pysh import core
from pysh.pysh import parser, state
from pysh.pysh.vals.builtins import type as type_builtin
from pysh.pysh.vals import type as type_lib
from pysh.pysh.exprs import expr, ref
from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Decl(statement.Statement):
    type: ref.Ref
    lhs: ref.Ref
    rhs: expr.Expr

    def _str_line(self) -> str:
        return f"{self.lhs}: {self.type} = {self.rhs};"

    def eval(self, state: state.State) -> result.Result:
        if not isinstance(
            type_ := cast(type_lib.Type, self.type.eval(state)),
            type_lib.Type,
        ):
            raise self._error(msg=f"decl has non-type type {self.type} = {type_}")
        self._try(lambda: type_builtin.type_.assert_can_assign(type_))
        self._try(lambda: self.lhs.set(state.scope, self.rhs.eval(state)))
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
