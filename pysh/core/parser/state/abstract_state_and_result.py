from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from pysh.core.parser.state import state_and_no_result
from pysh.core.parser.state import state

_Result = TypeVar("_Result")


@dataclass(frozen=True)
class AbstractStateAndResult(ABC, Generic[_Result]):
    state: state.State

    @abstractmethod
    def no(self) -> "state_and_no_result.StateAndNoResult[_Result]":
        ...

    @abstractmethod
    def single(self) -> "state_and_single_result.StateAndSingleResult[_Result]":
        ...


from pysh.core.parser.state import state_and_single_result
