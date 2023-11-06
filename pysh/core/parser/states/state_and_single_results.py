from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state_and_results


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class StateAndSingleResults(
    Generic[_State, _Result],
    state_and_results.StateAndResults[_State, results.SingleResults[_Result], _Result],
):
    def convert(
        self, func: Callable[[_Result], _ConvertResult]
    ) -> "StateAndSingleResults[_State,_ConvertResult]":
        return StateAndSingleResults[_State, _ConvertResult](
            self.state, self.results.convert(func)
        )
