from dataclasses import dataclass
from typing import Optional, TypeVar

from pysh.core.parser.state import (
    abstract_state_and_result,
    state_and_no_result,
    state_and_single_result,
    state_error,
)

_Result = TypeVar("_Result")


@dataclass(frozen=True)
class StateAndOptionalResult(abstract_state_and_result.AbstractStateAndResult[_Result]):
    result: Optional[_Result]

    def no(self) -> state_and_no_result.StateAndNoResult[_Result]:
        return state_and_no_result.StateAndNoResult[_Result](self.state)

    def single(self) -> state_and_single_result.StateAndSingleResult[_Result]:
        if not self.result:
            raise state_error.StateError(
                state=self.state,
                msg="unable to convert StateAndOptionalResult to StateAndSingleResult: no state",
            )
        return state_and_single_result.StateAndSingleResult[_Result](
            self.state, self.result
        )
