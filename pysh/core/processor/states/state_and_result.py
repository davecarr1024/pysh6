from dataclasses import dataclass
from typing import Generic
from pysh.core.processor import results as results_lib

from pysh.core.processor.states import state as state_lib


@dataclass(frozen=True)
class StateAndResult(Generic[state_lib.State, results_lib.Result]):
    state: state_lib.State
    results: results_lib.Results[results_lib.Result]

    def no(
        self,
    ) -> "state_and_no_result.StateAndNoResult[state_lib.State,results_lib.Result]":
        return state_and_no_result.StateAndNoResult[
            state_lib.State, results_lib.Result
        ](self.state, self.results.no())

    def single(
        self,
    ) -> "state_and_single_result.StateAndSingleResult[state_lib.State,results_lib.Result]":
        return state_and_single_result.StateAndSingleResult[
            state_lib.State, results_lib.Result
        ](self.state, self.results.single())

    def optional(
        self,
    ) -> "state_and_optional_result.StateAndOptionalResult[state_lib.State,results_lib.Result]":
        return state_and_optional_result.StateAndOptionalResult[
            state_lib.State, results_lib.Result
        ](self.state, self.results.optional())


from pysh.core.processor.states import (
    state_and_no_result,
    state_and_single_result,
    state_and_optional_result,
)
