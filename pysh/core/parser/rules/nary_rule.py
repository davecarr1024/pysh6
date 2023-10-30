from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Sequence, Sized, Type
from pysh.core import lexer

from pysh.core.parser import errors, results
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

    def _num_children_of_type(self, type: Type) -> int:
        num: int = 0
        for rule in self:
            if isinstance(rule, type):
                num += 1
        return num

    def _assert_num_children_of_type(self, type: Type, expected: int):
        actual = self._num_children_of_type(type)
        if actual != expected:
            raise errors.RuleError(
                rule=self,
                msg=f"num children of type {type} {actual} != expected {expected}",
            )
