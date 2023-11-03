from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Optional, overload
from pysh.core.parser.results import converter_result, result


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
    def named(
        self, name: Optional[str] = None
    ) -> "named_result.NamedResult[result.Result]":
        ...

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

    @abstractmethod
    def convert(
        self, func: Callable[..., result.Result]
    ) -> "single_result.SingleResult[result.Result]":
        ...

    @abstractmethod
    def convert_type(
        self, func: Callable[..., converter_result.ConverterResult]
    ) -> "single_result.SingleResult[converter_result.ConverterResult]":
        ...


from pysh.core.parser.results import (
    or_args,
    no_result,
    single_result,
    optional_result,
    multiple_result,
    named_result,
)
