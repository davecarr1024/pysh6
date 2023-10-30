from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Self, overload

from pysh.core.parser.results import result


@dataclass(frozen=True)
class Results(ABC, Generic[result.Result]):
    @abstractmethod
    def no(self) -> "no_result.NoResult[result.Result]":
        ...

    @abstractmethod
    def single(self) -> "single_result.SingleResult[result.Result]":
        ...

    @abstractmethod
    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        ...

    @abstractmethod
    def multiple(self) -> "multiple_result.MultipleResult[result.Result]":
        ...

    @abstractmethod
    def named(self, name: str) -> "named_result.NamedResult[result.Result]":
        ...

    def convert(
        self, func: Callable[[Self], "single_result.SingleResult[result.Result]"]
    ) -> "single_result.SingleResult[result.Result]":
        return func(self)

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "no_result.NoResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "single_result.SingleResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "optional_result.OptionalResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "multiple_result.MultipleResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "named_result.NamedResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @abstractmethod
    def __or__(
        self,
        rhs: "or_args.OrArgs",
    ) -> "Results[result.Result]":
        ...


from pysh.core.parser.results import (
    or_args,
    no_result,
    single_result,
    optional_result,
    multiple_result,
    named_result,
)
