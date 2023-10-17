from dataclasses import dataclass
from typing import TypeVar

from pysh.core.parser.state import (
    abstract_state_and_result,
    state_and_single_result,
    state_error,
)

_Result = TypeVar("_Result")


@dataclass(frozen=True)
class StateAndNoResult(abstract_state_and_result.AbstractStateAndResult[_Result]):
    def no(self) -> "StateAndNoResult[_Result]":
        return self

    def single(self) -> "state_and_single_result.StateAndSingleResult[_Result]":
        raise state_error.StateError(
            state=self.state,
            msg="unable to convert StateAndNoResult to StateAndSingleResult",
        )
