from dataclasses import dataclass
from pysh.core import lexer, tokens
from pysh.core.parser import results

from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class Literal(rule.Rule[results.Result]):
    lexer_rule: lexer.Rule

    def __str__(self) -> str:
        return repr(str(self.lexer_rule))

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer([self.lexer_rule])
