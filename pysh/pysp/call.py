from dataclasses import dataclass, field
from typing import Sequence
from pysh import core
from pysh.pysp import expr, parser, scope, val


@dataclass(frozen=True)
class Call(expr.Expr):
    operator: expr.Expr
    operands: Sequence[expr.Expr] = field(default_factory=list[expr.Expr])

    def eval(self, scope: scope.Scope) -> val.Val:
        return self.operator.eval(scope).apply(
            [operand.eval(scope) for operand in self.operands], scope
        )

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Call"]:
        return (
            r"\("
            & expr.Expr.ref().named("operator")
            & expr.Expr.ref()
            .zero_or_more()
            .convert(lambda values: values)
            .named("operands")
            & r"\)"
        ).convert(Call)
