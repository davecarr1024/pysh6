from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Sequence, Sized, Type, TypeVar
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ChildRuleType = TypeVar("_ChildRuleType", bound=rule.Rule, covariant=True)


@dataclass(frozen=True)
class NaryRule(
    Generic[_State, _Result, _ChildRuleType],
    rule.Rule[_State, _Result],
    Sized,
    Iterable[_ChildRuleType],
):
    _children: Sequence[_ChildRuleType] = field(default_factory=list[_ChildRuleType])

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Iterator[_ChildRuleType]:
        return iter(self._children)

    def _num_children_of_type(
        self, child_type: Type[rule.Rule[_State, _Result]]
    ) -> int:
        return sum(isinstance(child, child_type) for child in self)
