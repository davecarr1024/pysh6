from dataclasses import dataclass, field
from typing import Callable, Optional, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state, state_and_results


_State = TypeVar("_State", bound=state.State)
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class StateAndOptionalResults(
    state_and_results.StateAndResults[_State, _Result],
):
    results: "results.OptionalResults[_Result]" = field(
        default_factory=results.OptionalResults[_Result]
    )

    def convert(
        self, func: Callable[[Optional[_Result]], _RhsResult]
    ) -> "state_and_single_results.StateAndSingleResults[_State,_RhsResult]":
        return state_and_single_results.StateAndSingleResults[_State, _RhsResult](
            self.state, self.results.convert(func)
        )


from pysh.core.parser.states import state_and_single_results
