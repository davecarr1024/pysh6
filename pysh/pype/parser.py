from dataclasses import dataclass, field
from typing import Optional
from pysh import core


@dataclass(frozen=True)
class Parser(core.parser.states.State):
    statement_scope: core.parser.rules.Scope["Parser", "statement.Statement"] = field(
        default_factory=lambda: statement.Statement.parser_scope(),
        compare=False,
        repr=False,
        hash=False,
    )

    expr_scope: core.parser.rules.Scope["Parser", "expr.Expr"] = field(
        default_factory=lambda: expr.Expr.parser_scope(),
        compare=False,
        repr=False,
        hash=False,
    )

    val_scope: core.parser.rules.Scope["Parser", "val.Val"] = field(
        default_factory=lambda: val.Val.parser_scope(),
        compare=False,
        repr=False,
        hash=False,
    )

    def with_lexer_result(self, lexer_result: core.lexer.Result) -> "Parser":
        return Parser(
            lexer_result,
            self.statement_scope,
            self.expr_scope,
            self.val_scope,
        )

    @staticmethod
    def eval(input: str, scope_: Optional["scope.Scope"] = None) -> "val.Val":
        rule = (
            (statement.Statement.ref() & statement.Statement.ref().until_empty())
            .with_lexer(statement.Statement.lexer())
            .with_lexer(expr.Expr.lexer())
            .with_lexer(val.Val.lexer())
            .with_lexer(core.lexer.Lexer([core.lexer.Rule.load("~ws", r"\s+")]))
        )
        state = Parser(rule.lexer()(core.lexer.State.load(input)))
        statements = list[statement.Statement](rule(state).results)
        scope_ = scope_ or scope.Scope()
        for statement_ in statements[:-1]:
            statement_.eval(scope_)
        last_statement = statements[-1]
        if isinstance(last_statement, expr_statement.ExprStatement):
            return last_statement.value.eval(scope_)
        return builtins.none


from pysh.pype.statements import expr_statement, statement
from pysh.pype.exprs import expr
from pysh.pype.vals import builtins, scope, val
