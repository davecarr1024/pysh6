from dataclasses import dataclass, field
from typing import Iterator, Mapping

from pysh.core.parser.state_and_result import (
    result,
    state_and_multiple_results,
    state_and_no_result,
    state_and_optional_result,
    state_and_result,
    state_and_result_error,
    state_and_single_result,
)


@dataclass(frozen=True)
class StateAndNamedResults(
    state_and_result.StateAndResult[result.Result],
    Mapping[str, result.Result],
):
    _results: Mapping[str, result.Result] = field(
        default_factory=dict[str, result.Result]
    )

    def __getitem__(self, key: str) -> result.Result:
        if key not in self._results:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self, msg=f"unknown named result {key}"
            )
        return self._results[key]

    def __len__(self) -> int:
        return len(self._results)

    def __iter__(self) -> Iterator[str]:
        return iter(self._results)

    def no(self) -> state_and_no_result.StateAndNoResult[result.Result]:
        return state_and_no_result.StateAndNoResult[result.Result](self.state)

    def single(self) -> state_and_single_result.StateAndSingleResult[result.Result]:
        if len(self) != 1:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self,
                msg=f"unable to convert StateAndNamedResults to StateAndSingleResult: invalid result count {len(self)}",
            )
        return state_and_single_result.StateAndSingleResult[result.Result](
            self.state, list(self._results.values())[0]
        )

    def optional(
        self,
    ) -> state_and_optional_result.StateAndOptionalResult[result.Result]:
        if len(self) > 1:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self,
                msg=f"unable to convert StateAndNamedResults to StateAndOptionalResult: invalid result count {len(self)}",
            )
        elif len(self) == 1:
            return state_and_optional_result.StateAndOptionalResult[result.Result](
                self.state, list(self._results.values())[0]
            )
        else:
            return state_and_optional_result.StateAndOptionalResult[result.Result](
                self.state
            )

    def multiple(
        self,
    ) -> state_and_multiple_results.StateAndMultipleResults[result.Result]:
        return state_and_multiple_results.StateAndMultipleResults[result.Result](
            self.state, list(self._results.values())
        )

    def named(self, name: str) -> "StateAndNamedResults[result.Result]":
        return self
