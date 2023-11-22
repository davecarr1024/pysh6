from dataclasses import dataclass
from typing import cast
from pysh import core
from pysh.pysh import lexer, parser, state
from pysh.pysh.vals import arg, type, var
from pysh.pysh.exprs import ref


@dataclass(frozen=True)
class Param(
    core.errors.Errorable["Param"],
):
    type: ref.Ref
    name: str

    def __str__(self) -> str:
        return f"{self.name}: {self.type}"

    def bind(self, state: state.State, arg: arg.Arg) -> var.Var:
        if not isinstance(type_ := self.type.eval(state), type.Type):
            raise self._error(msg=f"param type {type_} is not a type")
        return var.Var(cast(type.Type, type_), arg.val)

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Param"]:
        return (lexer.id.named("name") & ":" & ref.Ref.ref().named("type")).convert(
            Param
        )
