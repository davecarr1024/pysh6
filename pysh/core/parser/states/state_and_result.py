from dataclasses import dataclass
from typing import Generic
from pysh.core.parser import results as results_lib

from pysh.core.parser.states import state as state_lib


@dataclass(frozen=True)
class StateAndResult(Generic[results_lib.Result]):
    state: state_lib.State
    results: results_lib.Results[results_lib.Result]

    def no(
        self,
    ) -> "state_and_no_result.StateAndNoResult[results_lib.Result]":
        return state_and_no_result.StateAndNoResult[results_lib.Result](
            self.state, self.results.no()
        )

    def single(
        self,
    ) -> "state_and_single_result.StateAndSingleResult[results_lib.Result]":
        return state_and_single_result.StateAndSingleResult[results_lib.Result](
            self.state, self.results.single()
        )

    def optional(
        self,
    ) -> "state_and_optional_result.StateAndOptionalResult[results_lib.Result]":
        return state_and_optional_result.StateAndOptionalResult[results_lib.Result](
            self.state, self.results.optional()
        )


from pysh.core.parser.states import (
    state_and_no_result,
    state_and_single_result,
    state_and_optional_result,
)
