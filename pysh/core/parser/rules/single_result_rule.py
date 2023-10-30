from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class SingleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State"
    ) -> "states.StateAndSingleResult[results.Result]":
        ...

    def single(self) -> "SingleResultRule[results.Result]":
        return self


from pysh.core.parser import states
