from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar, Union, overload


_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class Results(ABC, Generic[_Result]):
    @abstractmethod
    def no(self) -> "no_results.NoResults[_Result]":
        ...

    @abstractmethod
    def single(self) -> "single_results.SingleResults[_Result]":
        ...

    @abstractmethod
    def optional(self) -> "optional_results.OptionalResults[_Result]":
        ...

    @abstractmethod
    def multiple(self) -> "multiple_results.MultipleResults[_Result]":
        ...

    @abstractmethod
    def named(self, name: str = "") -> "named_results.NamedResults[_Result]":
        ...

    def _error(self, msg: str) -> "error.Error":
        return error.Error(results=self, msg=msg)

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "no_results.NoResults[_RhsResult]"
    ) -> "Results[_Result|_RhsResult]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "single_results.SingleResults[_RhsResult]"
    ) -> "Results[_Result|_RhsResult]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "optional_results.OptionalResults[_RhsResult]"
    ) -> "Results[_Result|_RhsResult]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "multiple_results.MultipleResults[_RhsResult]"
    ) -> "Results[_Result|_RhsResult]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "named_results.NamedResults[_RhsResult]"
    ) -> "Results[_Result|_RhsResult]":
        ...

    @abstractmethod
    def __or__(
        self,
        rhs: Union[
            "no_results.NoResults[_RhsResult]",
            "single_results.SingleResults[_RhsResult]",
            "optional_results.OptionalResults[_RhsResult]",
            "multiple_results.MultipleResults[_RhsResult]",
            "named_results.NamedResults[_RhsResult]",
        ],
    ) -> "Results[_Result|_RhsResult]":
        ...


from pysh.core.parser.results import (
    error,
    no_results,
    single_results,
    optional_results,
    multiple_results,
    named_results,
)
