from dataclasses import dataclass
from pysh import core
from pysh.pysp import expr, parser, scope, val


@dataclass(frozen=True)
class Literal(expr.Expr):
    value: val.Val

    def eval(self, scope: scope.Scope) -> val.Val:
        return self.value

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Literal"]:
        return val.Val.ref().convert(Literal)
