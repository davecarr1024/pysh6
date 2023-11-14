from dataclasses import dataclass, field
from typing import Iterator, Mapping, TypeVar
from pysh.core import errors
from pysh.core.parser import states


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class Scope(
    Mapping[str, "single_results_rule.SingleResultsRule[_State,_Result]"],
):
    _rules: Mapping[
        str, "single_results_rule.SingleResultsRule[_State,_Result]"
    ] = field(
        default_factory=lambda: dict[
            str, single_results_rule.SingleResultsRule[_State, _Result]
        ]()
    )

    def __str__(self) -> str:
        return f'Scope({",".join(f"{name} = {rule}" for name, rule in self.items())})'

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self._rules)

    def __getitem__(
        self, name: str
    ) -> "single_results_rule.SingleResultsRule[_State,_Result]":
        if name not in self._rules:
            raise errors.Error(msg=f"unknown rule {name}")
        return self._rules[name]


from pysh.core.parser.rules import single_results_rule
