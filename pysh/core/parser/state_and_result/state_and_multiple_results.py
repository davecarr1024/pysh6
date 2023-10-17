from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized

from pysh.core.parser.state_and_result import (
    abstract_state_and_result,
    result,
    state_and_named_results,
    state_and_no_result,
    state_and_optional_result,
    state_and_result_error,
    state_and_single_result,
)


@dataclass(frozen=True)
class StateAndMultipleResults(
    abstract_state_and_result.AbstractStateAndResult[result.Result],
    Sized,
    Iterable[result.Result],
):
    _results: Sequence[result.Result] = field(default_factory=list[result.Result])

    def __len__(self) -> int:
        return len(self._results)

    def __iter__(self) -> Iterator[result.Result]:
        return iter(self._results)

    def no(self) -> state_and_no_result.StateAndNoResult[result.Result]:
        return state_and_no_result.StateAndNoResult[result.Result](self.state)

    def single(self) -> state_and_single_result.StateAndSingleResult[result.Result]:
        if len(self._results) != 1:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self,
                msg=f"unable to convert StateAndMultipleResults to StateAndSingleResult: incorrect result count {len(self._results)}",
            )
        return state_and_single_result.StateAndSingleResult[result.Result](
            self.state, self._results[0]
        )

    def optional(
        self,
    ) -> state_and_optional_result.StateAndOptionalResult[result.Result]:
        if len(self._results) > 1:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self,
                msg=f"unable to convert StateAndMultipleResults to StateAndOptionalResult: incorrect result count {len(self._results)}",
            )
        elif len(self._results) == 1:
            return state_and_optional_result.StateAndOptionalResult[result.Result](
                self.state, self._results[0]
            )
        else:
            return state_and_optional_result.StateAndOptionalResult[result.Result](
                self.state
            )

    def multiple(self) -> "StateAndMultipleResults[result.Result]":
        return self

    def named(
        self, name: str
    ) -> state_and_named_results.StateAndNamedResults[result.Result]:
        if len(self) > 1:
            raise state_and_result_error.StateAndResultError(
                state_and_result=self,
                msg=f"unable to convert StateAndMultipleResults to StateAndNamedResults: incorrect result count {len(self._results)}",
            )
        elif len(self) == 0:
            return state_and_named_results.StateAndNamedResults[result.Result](
                self.state
            )
        else:
            return state_and_named_results.StateAndNamedResults[result.Result](
                self.state, {name: self._results[0]}
            )
