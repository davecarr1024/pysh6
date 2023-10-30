from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule, scope


@dataclass(frozen=True)
class MultipleResultsRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndMultipleResults[results.Result]:
        ...

    def multiple(self) -> "MultipleResultsRule[results.Result]":
        return self