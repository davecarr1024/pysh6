from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class SingleResultsRule(
    Generic[_State, _Result],
    rule.Rule[_State, results.SingleResults[_Result], _Result],
):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        ...
