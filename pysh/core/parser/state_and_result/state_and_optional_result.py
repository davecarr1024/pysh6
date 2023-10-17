from dataclasses import dataclass
from typing import Optional

from pysh.core.parser.state_and_result import (
    abstract_state_and_result,
    result,
    state_and_multiple_results,
    state_and_named_results,
    state_and_no_result,
    state_and_result_error,
    state_and_single_result,
    state_and_result_error,
)


@dataclass(frozen=True)
class StateAndOptionalResult(
    abstract_state_and_result.AbstractStateAndResult[result.Result]
):
    result_: Optional[result.Result] = None

    def no(self) -> state_and_no_result.StateAndNoResult[result.Result]:
        return state_and_no_result.StateAndNoResult[result.Result](self.state)

    def single(self) -> state_and_single_result.StateAndSingleResult[result.Result]:
        if not self.result_:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self,
                msg="unable to convert StateAndOptionalResult to StateAndSingleResult: no state",
            )
        return state_and_single_result.StateAndSingleResult[result.Result](
            self.state, self.result_
        )

    def optional(self) -> "StateAndOptionalResult[result.Result]":
        return self

    def multiple(
        self,
    ) -> state_and_multiple_results.StateAndMultipleResults[result.Result]:
        if self.result_ is None:
            return state_and_multiple_results.StateAndMultipleResults[result.Result](
                self.state, []
            )
        else:
            return state_and_multiple_results.StateAndMultipleResults[result.Result](
                self.state, [self.result_]
            )

    def named(
        self, name: str
    ) -> state_and_named_results.StateAndNamedResults[result.Result]:
        if self.result_ is None:
            return state_and_named_results.StateAndNamedResults[result.Result](
                self.state
            )
        else:
            return state_and_named_results.StateAndNamedResults[result.Result](
                self.state, {name: self.result_}
            )
