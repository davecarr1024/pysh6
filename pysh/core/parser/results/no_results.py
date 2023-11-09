from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_RhsResult = TypeVar("_RhsResult")


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
    def __or__(self, rhs: "NoResults[_RhsResult]") -> "NoResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_RhsResult]"
    ) -> "single_results.SingleResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_RhsResult]"
    ) -> "optional_results.OptionalResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results.MultipleResults[_RhsResult]"
    ) -> "multiple_results.MultipleResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "named_results.NamedResults[_RhsResult]"
    ) -> "named_results.NamedResults[_Result|_RhsResult]":
        ...

    def __or__(
        self,
        rhs: Union[
            "NoResults[_RhsResult]",
            "single_results.SingleResults[_RhsResult]",
            "optional_results.OptionalResults[_RhsResult]",
            "multiple_results.MultipleResults[_RhsResult]",
            "named_results.NamedResults[_RhsResult]",
        ],
    ) -> results.Results[_Result | _RhsResult]:
        match rhs:
            case NoResults():
                return NoResults[_Result | _RhsResult]()
            case single_results.SingleResults():
                return single_results.SingleResults[_Result | _RhsResult](rhs.value)
            case optional_results.OptionalResults():
                return optional_results.OptionalResults[_Result | _RhsResult](rhs.value)
            case multiple_results.MultipleResults():
                return multiple_results.MultipleResults[_Result | _RhsResult](
                    rhs._values
                )
            case named_results.NamedResults():
                return named_results.NamedResults[_Result | _RhsResult](rhs._values)
            case _:
                raise self._error(f"unknown rhs {rhs}")

    def convert(
        self, func: Callable[[], _RhsResult]
    ) -> "single_results.SingleResults[_RhsResult]":
        return single_results.SingleResults[_RhsResult](func())


from pysh.core.parser.results import (
    single_results,
    optional_results,
    multiple_results,
    named_results,
)
