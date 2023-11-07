from dataclasses import dataclass
from typing import Callable, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state_and_results


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class StateAndSingleResults(
    state_and_results.StateAndResults[_State, _Result],
):
    results: "results.SingleResults[_Result]"

    def convert(
        self, func: Callable[[_Result], _ConvertResult]
    ) -> "StateAndSingleResults[_State,_ConvertResult]":
        return StateAndSingleResults[_State, _ConvertResult](
            self.state, self.results.convert(func)
        )
