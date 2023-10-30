from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional
from pysh.core.parser import results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class NamedResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndNamedResult[results.Result]":
        ...

    def named(self, name: Optional[str] = None) -> "NamedResultRule[results.Result]":
        return self


from pysh.core.parser import states
