from dataclasses import dataclass
from typing import Generic

from pysh.core import lexer
from pysh.core.parser.rules import child_rule


@dataclass(frozen=True)
class UnaryRule(Generic[child_rule.ChildRule]):
    child: child_rule.ChildRule

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
