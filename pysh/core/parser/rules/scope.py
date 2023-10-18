from dataclasses import dataclass, field
from typing import Generic, Iterator, Mapping
from pysh.core.parser import errors, results, states


@dataclass(frozen=True)
class Scope(
    Generic[results.Result],
    Mapping[str, "rule.Rule[ results.Result]"],
):
    _rules: Mapping[str, "rule.Rule[results.Result]"] = field(
        default_factory=lambda: dict[str, rule.Rule[results.Result]]()
    )

    def __getitem__(self, key: str) -> "rule.Rule[results.Result]":
        if key not in self._rules:
            raise errors.Error(msg=f"unknown rule {key}")
        return self._rules[key]

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self._rules)


from pysh.core.parser.rules import rule
