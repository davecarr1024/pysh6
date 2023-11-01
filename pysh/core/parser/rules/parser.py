from dataclasses import dataclass
from pysh.core import lexer
from pysh.core.parser import results
from pysh.core.parser.rules import scope, single_result_rule


@dataclass(frozen=True)
class Parser(single_result_rule.SingleResultRule[results.Result]):
    scope: scope.Scope[results.Result]
    root_rule_name: str

    def lexer(self) -> lexer.Lexer:
        lexer_ = lexer.Lexer()
        for rule in self.scope.values():
            lexer_ |= rule.lexer()
        return lexer_
