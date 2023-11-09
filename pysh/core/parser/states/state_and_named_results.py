from dataclasses import dataclass, field
from typing import Callable, Mapping, TypeVar
from pysh.core.parser import results
from pysh.core.parser.states import state_and_results


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class StateAndNamedResults(
    state_and_results.StateAndResults[_State, _Result],
):
    results: "results.NamedResults[_Result]" = field(
        default_factory=results.NamedResults[_Result]
    )

    def convert(
        self, func: Callable[..., _RhsResult]
    ) -> "state_and_single_results.StateAndSingleResults[_State,_RhsResult]":
        return state_and_single_results.StateAndSingleResults[_State, _RhsResult](
            self.state, self.results.convert(func)
        )


from pysh.core.parser.states import state_and_single_results
