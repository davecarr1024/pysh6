from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.states import state


_State = TypeVar("_State", bound=state.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class StateAndResults(
    Generic[_State, _Result],
    errors.Errorable["StateAndResults"],
):
    state: _State
    results: results.Results[_Result]

    def __str__(self) -> str:
        return f"StateAndResults(state={self.state},results={self.results})"

    def no(self) -> "state_and_no_results.StateAndNoResults[_State,_Result]":
        return state_and_no_results.StateAndNoResults[_State, _Result](
            self.state, self.results.no()
        )

    def single(
        self,
    ) -> "state_and_single_results.StateAndSingleResults[_State,_Result]":
        return state_and_single_results.StateAndSingleResults[_State, _Result](
            self.state, self.results.single()
        )

    def optional(
        self,
    ) -> "state_and_optional_results.StateAndOptionalResults[_State,_Result]":
        return state_and_optional_results.StateAndOptionalResults[_State, _Result](
            self.state, self.results.optional()
        )

    def multiple(
        self,
    ) -> "state_and_multiple_results.StateAndMultipleResults[_State,_Result]":
        return state_and_multiple_results.StateAndMultipleResults[_State, _Result](
            self.state, self.results.multiple()
        )

    def named(
        self, name: str = ""
    ) -> "state_and_named_results.StateAndNamedResults[_State,_Result]":
        return state_and_named_results.StateAndNamedResults[_State, _Result](
            self.state, self.results.named(name)
        )


from pysh.core.parser.states import (
    state_and_no_results,
    state_and_single_results,
    state_and_optional_results,
    state_and_multiple_results,
    state_and_named_results,
)
