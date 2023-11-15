from dataclasses import dataclass
from typing import Sequence
from pysh import core
from pysh.pysp import error, id, parser, val


@dataclass(frozen=True)
class Func(val.Val):
    params: Sequence[str]
    body: "expr.Expr"

    def apply(self, args: Sequence[val.Val], scope_: "scope.Scope") -> val.Val:
        if len(self.params) != len(args):
            raise error.Error(
                msg=f"func {self} expected {len(self.params)} args but got {len(args)}"
            )
        return self.body.eval(
            scope.Scope(
                {param: arg for param, arg in zip(self.params, args)},
                scope_,
            ),
        )

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Func"]:
        return (
            r"\("
            & core.parser.rules.Literal[parser.Parser].load("lambda").no()
            & (
                r"\("
                & core.parser.rules.Literal[parser.Parser](id.id_lexer_rule)
                .token_value()
                .zero_or_more()
                & r"\)"
            )
            .convert(lambda params: params)
            .named("params")
            & expr.Expr.ref().named("body")
            & r"\)"
        ).convert(Func)


from pysh.pysp import expr, scope
