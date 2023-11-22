from dataclasses import dataclass, field
from typing import Optional
from pysh import core


@dataclass(frozen=True)
class Parser(core.parser.states.State):
    expr_scope: core.parser.rules.Scope["Parser", "expr.Expr"] = field(
        default_factory=lambda: expr.Expr.parser_scope(),
        repr=False,
        compare=False,
        hash=False,
    )

    statement_scope: core.parser.rules.Scope["Parser", "statement.Statement"] = field(
        default_factory=lambda: statement.Statement.parser_scope(),
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
    def eval(input: str, scope_: Optional["scope.Scope"] = None) -> "val.Val":
        rule = (
            (statement.Statement.ref() & statement.Statement.ref().until_empty())
            .with_lexer(statement.Statement.lexer())
            .with_lexer(expr.Expr.lexer())
            .with_lexer(core.lexer.Lexer([core.lexer.Rule.load("~ws", r"\s+")]))
        ).convert(block.Block)
        parser = Parser(rule.lexer()(input))
        block_: block.Block = rule(parser).results.value
        state_ = state.State(scope_ or scope.Scope())
        return block_.eval(state_).return_value or none_.none


from .exprs import expr
from .statements import block, statement
from .vals.builtins import none_
from .vals import scope, val
from . import state
