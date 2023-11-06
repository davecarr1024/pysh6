from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class OptionalResultsRule(
    Generic[_State, _Result],
    rule.Rule[_State, results.OptionalResults[_Result], _Result],
):
    @abstractmethod
    def __call__(
        self, state: _State
    ) -> states.StateAndOptionalResults[_State, _Result]:
        ...
