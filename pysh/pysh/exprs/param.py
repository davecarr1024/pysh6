from dataclasses import dataclass
from pysh import core
from pysh.pysh import lexer, parser, state
from pysh.pysh.vals import param, type
from pysh.pysh.exprs import ref


@dataclass(frozen=True)
class Param(
    core.errors.Errorable["Param"],
):
    type: ref.Ref
    name: str

    def __str__(self) -> str:
        return f"{self.name}: {self.type}"

    def bind(self, state: state.State) -> param.Param:
        if not isinstance(type_ := self.type.eval(state), type.Type):
            raise self._error(msg=f"invalid type {type_}")
        return param.Param(type_, self.name)

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Param"]:
        return (lexer.id.named("name") & ":" & ref.Ref.ref().named("type")).convert(
            Param
        )
