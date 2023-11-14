from dataclasses import dataclass, field
from typing import Callable, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state, state_and_results


_State = TypeVar("_State", bound=state.State)
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class StateAndNoResults(
    state_and_results.StateAndResults[_State, _Result],
):
    results: "results.NoResults[_Result]" = field(
        default_factory=results.NoResults[_Result]
    )

    def convert(
        self, func: Callable[[], _RhsResult]
    ) -> "state_and_single_results.StateAndSingleResults[_State,_RhsResult]":
        return state_and_single_results.StateAndSingleResults[_State, _RhsResult](
            self.state, self.results.convert(func)
        )


from pysh.core.parser.states import state_and_single_results
