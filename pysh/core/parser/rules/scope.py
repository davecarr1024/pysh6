from dataclasses import dataclass, field
from typing import Generic, Iterator, Mapping
from pysh.core.parser import errors, results


@dataclass(frozen=True)
class Scope(
    Generic[results.Result],
    Mapping[str, "single_result_rule.SingleResultRule[ results.Result]"],
):
    _rules: Mapping[str, "single_result_rule.SingleResultRule[results.Result]"] = field(
        default_factory=lambda: dict[
            str, single_result_rule.SingleResultRule[results.Result]
        ]()
    )

    def __str__(self) -> str:
        return f'{{{", ".join([f"{name}: {str(rule)}" for name, rule in self._rules.items()])}}}'

    def __getitem__(
        self, key: str
    ) -> "single_result_rule.SingleResultRule[results.Result]":
        if key not in self._rules:
            raise errors.Error(msg=f"unknown rule {key}")
        return self._rules[key]

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self._rules)

    def __or__(self, rhs: "Scope[results.Result]") -> "Scope[results.Result]":
        return Scope[results.Result](dict(self) | dict(rhs))


from pysh.core.parser.rules import single_result_rule
