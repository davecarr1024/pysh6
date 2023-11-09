from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar
from pysh.core.parser import results


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class StateAndResults(ABC, Generic[_State, _Result]):
    state: _State
    results: results.Results[_Result]

    def __str__(self) -> str:
        return f"StateAndResults(state={self.state},results={self.results})"

    def _error(self, msg: Optional[str] = None) -> "error.Error":
        return error.Error(state_and_results=self, msg=msg)

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
        self,
    ) -> "state_and_named_results.StateAndNamedResults[_State,_Result]":
        return state_and_named_results.StateAndNamedResults[_State, _Result](
            self.state, self.results.named()
        )


from pysh.core.parser.states import (
    error,
    state_and_no_results,
    state_and_single_results,
    state_and_optional_results,
    state_and_multiple_results,
    state_and_named_results,
)
