from dataclasses import dataclass
from typing import Callable, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state_and_results


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class StateAndSingleResults(
    state_and_results.StateAndResults[_State, _Result],
):
    results: "results.SingleResults[_Result]"

    def convert(
        self, func: Callable[[_Result], _RhsResult]
    ) -> "StateAndSingleResults[_State,_RhsResult]":
        return StateAndSingleResults[_State, _RhsResult](
            self.state, self.results.convert(func)
        )
