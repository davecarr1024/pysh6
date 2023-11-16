from dataclasses import dataclass
from pysh import core
from pysh.pype import lexer, parser
from pysh.pype.exprs.ref.parts import part
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Member(part.Part):
    name: str

    def __str__(self) -> str:
        return f".{self.name}"

    def eval(self, scope: scope.Scope, val: val.Val) -> val.Val:
        return val[self.name]

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Member"]:
        return (
            r"\." & core.parser.rules.Literal[parser.Parser](lexer.id).token_value()
        ).convert(Member)
