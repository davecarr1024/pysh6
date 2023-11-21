from dataclasses import dataclass, field
from typing import Optional
from pysh import core
from pysh.core import lexer


@dataclass(frozen=True)
class Parser(core.parser.states.State):
    expr_scope: core.parser.rules.Scope["Parser", "exprs.Expr"] = field(
        default_factory=lambda: exprs.Expr.parser_scope(),
        repr=False,
        compare=False,
        hash=False,
    )

    statement_scope: core.parser.rules.Scope["Parser", "statements.Statement"] = field(
        default_factory=lambda: statements.Statement.parser_scope(),
        repr=False,
        compare=False,
        hash=False,
    )

    def with_lexer_result(self, lexer_result: core.lexer.Result) -> "Parser":
        return Parser(
            lexer_result,
            self.expr_scope,
        )

    @staticmethod
    def eval(input: str, scope: Optional["vals.Scope"] = None) -> "vals.Val":
        rule = (
            (statements.Statement.ref() & statements.Statement.ref().until_empty())
            .with_lexer(statements.Statement.lexer())
            .with_lexer(exprs.Expr.lexer())
            .with_lexer(core.lexer.Lexer([core.lexer.Rule.load("~ws", r"\s+")]))
        ).convert(statements.Block)
        state = Parser(rule.lexer()(input))
        block: statements.Block = rule(state).results.value
        return block.eval(scope or vals.Scope()).return_value or vals.none


from pysh.pysh import exprs, statements, vals
