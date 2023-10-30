from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class MultipleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndMultipleResult[results.Result]":
        ...

    def multiple(self) -> "MultipleResultRule[results.Result]":
        return self


from pysh.core.parser import states
