from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar, Union, overload


_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


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

    def _error(self, msg: Optional[str] = None) -> "error.Error":
        return error.Error(results=self, msg=msg)

    @overload
    @abstractmethod
    def __or__(self, rhs: "no_results.NoResults[_Result]"):
        ...

    @overload
    @abstractmethod
    def __or__(self, rhs: "single_results.SingleResults[_Result]"):
        ...

    @overload
    @abstractmethod
    def __or__(self, rhs: "optional_results.OptionalResults[_Result]"):
        ...

    @overload
    @abstractmethod
    def __or__(self, rhs: "multiple_results.MultipleResults[_Result]"):
        ...

    @overload
    @abstractmethod
    def __or__(self, rhs: "named_results.NamedResults[_Result]"):
        ...

    @abstractmethod
    def __or__(
        self,
        rhs: Union[
            "no_results.NoResults[_Result]",
            "single_results.SingleResults[_Result]",
            "optional_results.OptionalResults[_Result]",
            "multiple_results.MultipleResults[_Result]",
            "named_results.NamedResults[_Result]",
        ],
    ) -> "Results[_Result]":
        ...

    @abstractmethod
    def convert(
        self, func: Callable[..., _ConvertResult]
    ) -> "single_results.SingleResults[_ConvertResult]":
        ...


from pysh.core.parser.results import (
    error,
    no_results,
    single_results,
    optional_results,
    multiple_results,
    named_results,
)
