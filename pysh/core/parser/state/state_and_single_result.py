from dataclasses import dataclass
from typing import TypeVar

from pysh.core.parser.state import abstract_state_and_result, state_and_no_result

_Result = TypeVar("_Result")


@dataclass(frozen=True)
class StateAndSingleResult(abstract_state_and_result.AbstractStateAndResult[_Result]):
    result: _Result

    def no(self) -> state_and_no_result.StateAndNoResult[_Result]:
        return state_and_no_result.StateAndNoResult[_Result](self.state)

    def single(self) -> "StateAndSingleResult[_Result]":
        return self
