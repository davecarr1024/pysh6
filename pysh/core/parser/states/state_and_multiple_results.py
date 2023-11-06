from dataclasses import dataclass, field
from typing import Callable, Generic, Sequence, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state_and_results


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class StateAndMultipleResults(
    Generic[_State, _Result],
    state_and_results.StateAndResults[
        _State, results.MultipleResults[_Result], _Result
    ],
):
    def convert(
        self, func: Callable[[Sequence[_Result]], _ConvertResult]
    ) -> "state_and_single_results.StateAndSingleResults[_State,_ConvertResult]":
        return state_and_single_results.StateAndSingleResults[_State, _ConvertResult](
            self.state, self.results.convert(func)
        )


from pysh.core.parser.states import state_and_single_results
