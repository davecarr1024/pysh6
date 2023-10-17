from dataclasses import dataclass

from pysh.core.parser.state_and_result import (
    result,
    state_and_multiple_results,
    state_and_named_results,
    state_and_no_result,
    state_and_optional_result,
    state_and_result,
)


@dataclass(frozen=True)
class StateAndSingleResult(state_and_result.StateAndResult[result.Result]):
    result_: result.Result

    def no(self) -> state_and_no_result.StateAndNoResult[result.Result]:
        return state_and_no_result.StateAndNoResult[result.Result](self.state)

    def single(self) -> "StateAndSingleResult[result.Result]":
        return self

    def optional(
        self,
    ) -> "state_and_optional_result.StateAndOptionalResult[result.Result]":
        return state_and_optional_result.StateAndOptionalResult[result.Result](
            self.state, self.result_
        )

    def multiple(
        self,
    ) -> state_and_multiple_results.StateAndMultipleResults[result.Result]:
        return state_and_multiple_results.StateAndMultipleResults[result.Result](
            self.state, [self.result_]
        )

    def named(
        self, name: str
    ) -> state_and_named_results.StateAndNamedResults[result.Result]:
        return state_and_named_results.StateAndNamedResults[result.Result](
            self.state, {name: self.result_}
        )
