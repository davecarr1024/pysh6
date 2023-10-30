from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Sequence, Sized
from pysh.core import lexer

from pysh.core.parser import results
from pysh.core.parser.rules import child_rule, rule


@dataclass(frozen=True)
class NaryRule(
    Generic[results.Result, child_rule.ChildRule],
    rule.Rule[results.Result],
    Sized,
    Iterable[child_rule.ChildRule],
):
    _children: Sequence[child_rule.ChildRule] = field(
        default_factory=list[child_rule.ChildRule]
    )

    def __iter__(self) -> Iterator[child_rule.ChildRule]:
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)

    def lexer(self) -> lexer.Lexer:
        lexer_ = lexer.Lexer()
        for child in self:
            lexer_ |= child.lexer()
        return lexer_
