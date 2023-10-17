from dataclasses import dataclass, field
from typing import Generic, Iterator, Mapping, TypeVar
from pysh.core.parser import errors

_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Scope(Generic[_Result], Mapping[str, "rule.Rule[_Result]"]):
    _rules: Mapping[str, "rule.Rule[_Result]"] = field(
        default_factory=lambda: dict[str, rule.Rule[_Result]]()
    )

    def __getitem__(self, key: str) -> "rule.Rule[_Result]":
        if key not in self._rules:
            raise errors.Error(msg=f"unknown rule {key}")
        return self._rules[key]

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self._rules)


from pysh.core.parser.rules import rule
