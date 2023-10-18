from abc import ABC, abstractmethod
from typing import Generic

from pysh.core.processor import results, states
from pysh.core.processor.rules import scope


class Rule(ABC, Generic[states.State, results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[states.State, results.Result]
    ) -> states.StateAndResult[states.State, results.Result]:
        ...
