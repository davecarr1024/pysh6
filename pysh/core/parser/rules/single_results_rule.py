from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class SingleResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        ...
