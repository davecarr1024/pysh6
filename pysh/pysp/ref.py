from dataclasses import dataclass
from pysh import core

from pysh.pysp import expr, id, parser, scope, val


@dataclass(frozen=True)
class Ref(expr.Expr):
    name: str

    def eval(self, scope: scope.Scope) -> val.Val:
        return scope[self.name]

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref"]:
        return (
            core.parser.rules.Literal[parser.Parser]
            .load(id.id_lexer_rule)
            .token_value()
            .convert(Ref)
        )
