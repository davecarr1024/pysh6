from dataclasses import dataclass
from pysh import core
from pysh.pype import lexer, parser
from pysh.pype.exprs.refs.parts import part
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Member(part.Part):
    name: str

    def __str__(self) -> str:
        return f".{self.name}"

    def get(self, scope: scope.Scope, obj: val.Val) -> val.Val:
        return obj[self.name]

    def set(self, scope: scope.Scope, obj: val.Val, val: val.Val) -> None:
        obj[self.name] = val

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Member"]:
        return (
            r"\." & core.parser.rules.Literal[parser.Parser](lexer.id).token_value()
        ).convert(Member)
