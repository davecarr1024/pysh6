from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Optional
from pysh.core.parser import results as results_lib
from pysh.core.parser.states import state as state_lib


@dataclass(frozen=True)
class StateAndResult(Generic[results_lib.Result], ABC):
    state: state_lib.State
    results: results_lib.Results[results_lib.Result]

    def no(
        self,
    ) -> "state_and_no_result.StateAndNoResult[results_lib.Result]":
        return state_and_no_result.StateAndNoResult[results_lib.Result](
            self.state, self.results.no()
        )

    def single(
        self,
    ) -> "state_and_single_result.StateAndSingleResult[results_lib.Result]":
        return state_and_single_result.StateAndSingleResult[results_lib.Result](
            self.state, self.results.single()
        )

    def optional(
        self,
    ) -> "state_and_optional_result.StateAndOptionalResult[results_lib.Result]":
        return state_and_optional_result.StateAndOptionalResult[results_lib.Result](
            self.state, self.results.optional()
        )

    def multiple(
        self,
    ) -> "state_and_multiple_result.StateAndMultipleResult[results_lib.Result]":
        return state_and_multiple_result.StateAndMultipleResult[results_lib.Result](
            self.state, self.results.multiple()
        )

    def named(
        self, name: Optional[str] = None
    ) -> "state_and_named_result.StateAndNamedResult[results_lib.Result]":
        return state_and_named_result.StateAndNamedResult[results_lib.Result](
            self.state, self.results.named(name)
        )

    @abstractmethod
    def convert(
        self, func: Callable[..., results_lib.Result]
    ) -> "StateAndResult[results_lib.Result]":
        ...

    @abstractmethod
    def convert_type(
        self, func: Callable[..., results_lib.ConverterResult]
    ) -> "StateAndResult[results_lib.ConverterResult]":
        ...


from pysh.core.parser.states import (
    state_and_no_result,
    state_and_single_result,
    state_and_optional_result,
    state_and_multiple_result,
    state_and_named_result,
)
