from dataclasses import dataclass
from pysh.core import lexer, tokens
from pysh.core.parser import results

from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class Literal(rule.Rule[results.Result]):
    lexer_rule: lexer.Rule

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer([self.lexer_rule])
