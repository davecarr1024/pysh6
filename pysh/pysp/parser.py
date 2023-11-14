from dataclasses import dataclass, field
from pysh import core


@dataclass(frozen=True)
class Parser(core.parser.states.State):
    val_scope: core.parser.rules.Scope["Parser", "val.Val"] = field(
        compare=False,
        repr=False,
        hash=False,
        default_factory=lambda: val.Val.scope(),
    )

    expr_scope: core.parser.rules.Scope["Parser", "expr.Expr"] = field(
        compare=False,
        repr=False,
        hash=False,
        default_factory=lambda: expr.Expr.scope(),
    )

    def with_lexer_result(self, lexer_result: core.lexer.Result) -> "Parser":
        return Parser(lexer_result, self.val_scope)

    @staticmethod
    def load(*tokens: core.tokens.Token) -> "Parser":
        return Parser(core.lexer.Result(core.tokens.Stream(tokens)))

    @staticmethod
    def eval(input: str) -> "val.Val":
        rule = (
            (expr.Expr.ref() & expr.Expr.ref().until_empty())
            .with_lexer(expr.Expr.lexer())
            .with_lexer(val.Val.lexer())
            .with_lexer(core.lexer.Lexer([core.lexer.Rule.load("~ws", r"\s+")]))
        )
        state = Parser(rule.lexer()(core.lexer.State.load(input)))
        exprs = list[expr.Expr](rule(state).results)
        scope_ = scope.Scope()
        for expr_ in exprs[:-1]:
            expr_.eval(scope_)
        return exprs[-1].eval(scope_)


from pysh.pysp import expr, scope, val
