from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class NoResults(results.Results[_Result]):
    def no(self) -> "NoResults[_Result]":
        return self

    def single(self) -> "single_results.SingleResults[_Result]":
        raise self._error()

    def optional(self) -> "optional_results.OptionalResults[_Result]":
        return optional_results.OptionalResults[_Result]()

    def multiple(self) -> "multiple_results.MultipleResults[_Result]":
        return multiple_results.MultipleResults[_Result]()

    def named(self, name: str = "") -> "named_results.NamedResults[_Result]":
        return named_results.NamedResults[_Result]()

    @overload
    def __or__(self, rhs: "NoResults[_Result]") -> "NoResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_Result]"
    ) -> "single_results.SingleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_Result]"
    ) -> "optional_results.OptionalResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results.MultipleResults[_Result]"
    ) -> "multiple_results.MultipleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "named_results.NamedResults[_Result]"
    ) -> "named_results.NamedResults[_Result]":
        ...

    def __or__(
        self,
        rhs: Union[
            "NoResults[_Result]",
            "single_results.SingleResults[_Result]",
            "optional_results.OptionalResults[_Result]",
            "multiple_results.MultipleResults[_Result]",
            "named_results.NamedResults[_Result]",
        ],
    ) -> results.Results[_Result]:
        return rhs

    def convert(
        self, func: Callable[[], _ConvertResult]
    ) -> "single_results.SingleResults[_ConvertResult]":
        return single_results.SingleResults[_ConvertResult](func())


from pysh.core.parser.results import (
    single_results,
    optional_results,
    multiple_results,
    named_results,
)
