from dataclasses import dataclass, field
from typing import Generic, Iterator, Mapping, TypeVar
from pysh.core import errors
from pysh.core.parser import results


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Scope(
    Mapping[str, "rule.Rule[_State,_Result]"],
):
    _rules: Mapping[str, "rule.Rule[_State,_Result]"] = field(
        default_factory=lambda: dict[str, rule.Rule[_State, _Result]]()
    )

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self._rules)

    def __getitem__(self, name: str) -> "rule.Rule[_State,_Result]":
        if name not in self._rules:
            raise errors.Error(msg=f"unknown rule {name}")
        return self._rules[name]


from pysh.core.parser.rules import rule
