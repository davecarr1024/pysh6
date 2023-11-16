from dataclasses import dataclass
from pysh import core
from pysh.pype import lexer, parser
from pysh.pype.exprs.ref.roots import root
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Name(root.Root):
    name: str

    def eval(self, scope: scope.Scope) -> val.Val:
        return scope[self.name]

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Name"]:
        return (
            core.parser.rules.Literal[parser.Parser](lexer.id)
            .token_value()
            .convert(Name)
        )
