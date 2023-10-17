from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic

from pysh.core.parser.state_and_result import (
    result,
    state,
)


@dataclass(frozen=True)
class StateAndResult(ABC, Generic[result.Result]):
    state: state.State

    @abstractmethod
    def no(self) -> "state_and_no_result.StateAndNoResult[result.Result]":
        ...

    @abstractmethod
    def single(self) -> "state_and_single_result.StateAndSingleResult[result.Result]":
        ...

    @abstractmethod
    def optional(
        self,
    ) -> "state_and_optional_result.StateAndOptionalResult[result.Result]":
        ...

    @abstractmethod
    def multiple(
        self,
    ) -> "state_and_multiple_results.StateAndMultipleResults[result.Result]":
        ...

    @abstractmethod
    def named(
        self, name: str
    ) -> "state_and_named_results.StateAndNamedResults[result.Result]":
        ...


from pysh.core.parser.state_and_result import (
    state_and_multiple_results,
    state_and_named_results,
    state_and_no_result,
    state_and_single_result,
    state_and_optional_result,
)
