from dataclasses import dataclass
from typing import Generic

from pysh.core import lexer
from pysh.core.parser import results
from pysh.core.parser.rules import child_rule, rule


@dataclass(frozen=True)
class UnaryRule(
    Generic[results.Result, child_rule.ChildRule], rule.Rule[results.Result]
):
    child: child_rule.ChildRule

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
