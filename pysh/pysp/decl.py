from dataclasses import dataclass
from pysh import core
from pysh.pysp import expr, id, parser, scope, val


@dataclass(frozen=True)
class Decl(expr.Expr):
    name: str
    value: expr.Expr

    def eval(self, scope: scope.Scope) -> val.Val:
        value = scope[self.name] = self.value.eval(scope)
        return value

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Decl"]:
        return (
            r"\("
            & (
                "def"
                & core.parser.rules.Literal[parser.Parser](id.id_lexer_rule)
                .token_value()
                .named("name")
                & expr.Expr.ref().named("value")
            )
            & r"\)"
        ).convert(Decl)
