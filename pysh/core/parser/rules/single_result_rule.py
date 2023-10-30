from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule, scope


@dataclass(frozen=True)
class SingleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndSingleResult[results.Result]:
        ...

    def single(self) -> "SingleResultRule[results.Result]":
        return self
