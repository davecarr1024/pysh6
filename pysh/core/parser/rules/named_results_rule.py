from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class NamedResultsRule(
    Generic[_State, _Result],
    rule.Rule[_State, results.NamedResults[_Result], _Result],
):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndNamedResults[_State, _Result]:
        ...
