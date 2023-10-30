from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule, scope


@dataclass(frozen=True)
class NamedResultsRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndNamedResults[results.Result]:
        ...

    def named(self, name: str) -> "NamedResultsRule[results.Result]":
        return self
