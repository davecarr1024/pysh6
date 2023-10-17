from dataclasses import dataclass

from pysh.core.parser.state_and_result import (
    result,
    state_and_result,
    state_and_result_error,
)


@dataclass(frozen=True)
class StateAndNoResult(state_and_result.StateAndResult[result.Result]):
    def no(self) -> "StateAndNoResult[result.Result]":
        return self

    def single(self) -> "state_and_single_result.StateAndSingleResult[result.Result]":
        raise state_and_result_error.StateAndResultError(
            state_and_result=self,
            msg="unable to convert StateAndNoResult to StateAndSingleResult",
        )

    def optional(
        self,
    ) -> "state_and_optional_result.StateAndOptionalResult[result.Result]":
        return state_and_optional_result.StateAndOptionalResult[result.Result](
            self.state
        )

    def multiple(
        self,
    ) -> "state_and_multiple_results.StateAndMultipleResults[result.Result]":
        return state_and_multiple_results.StateAndMultipleResults[result.Result](
            self.state, []
        )

    def named(
        self, name: str
    ) -> "state_and_named_results.StateAndNamedResults[result.Result]":
        return state_and_named_results.StateAndNamedResults[result.Result](self.state)


from pysh.core.parser.state_and_result import (
    state_and_named_results,
    state_and_optional_result,
    state_and_single_result,
    state_and_multiple_results,
)
