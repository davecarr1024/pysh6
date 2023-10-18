from abc import ABC, abstractmethod
from typing import Generic

from pysh.core.parser import results, states
from pysh.core.parser.rules import scope


class Rule(ABC, Generic[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndResult[results.Result]:
        ...
