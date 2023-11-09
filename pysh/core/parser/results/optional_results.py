from dataclasses import dataclass
from typing import Callable, Optional, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class OptionalResults(results.Results[_Result]):
    value: Optional[_Result] = None

    def no(self) -> "no_results.NoResults[_Result]":
        return no_results.NoResults[_Result]()

    def single(self) -> "single_results.SingleResults[_Result]":
        match self.value:
            case None:
                raise self._error()
            case _:
                return single_results.SingleResults[_Result](self.value)

    def optional(self) -> "OptionalResults[_Result]":
        return self

    def multiple(self) -> "multiple_results.MultipleResults[_Result]":
        match self.value:
            case None:
                return multiple_results.MultipleResults[_Result]()
            case _:
                return multiple_results.MultipleResults[_Result]([self.value])

    def named(self, name: str = "") -> "named_results.NamedResults[_Result]":
        match self.value:
            case None:
                return named_results.NamedResults[_Result]()
            case _:
                return named_results.NamedResults[_Result]({name: self.value})

    @overload
    def __or__(
        self, rhs: "no_results.NoResults[_RhsResult]"
    ) -> "single_results.SingleResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_RhsResult]"
    ) -> "multiple_results.MultipleResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "OptionalResults[_RhsResult]"
    ) -> "multiple_results.MultipleResults[_Result|_RhsResult]":
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
            "no_results.NoResults[_RhsResult]",
            "single_results.SingleResults[_RhsResult]",
            "OptionalResults[_RhsResult]",
            "multiple_results.MultipleResults[_RhsResult]",
            "named_results.NamedResults[_RhsResult]",
        ],
    ) -> results.Results[_Result | _RhsResult]:
        match rhs:
            case no_results.NoResults():
                return OptionalResults[_Result | _RhsResult](self.value)
            case single_results.SingleResults() | OptionalResults() | multiple_results.MultipleResults():
                return multiple_results.MultipleResults[_Result | _RhsResult](
                    list(self.multiple()._values) + list(rhs.multiple()._values)
                )
            case named_results.NamedResults():
                return named_results.NamedResults[_Result | _RhsResult](
                    dict(self.named()._values) | dict(rhs._values)
                )
            case _:
                raise self._error(f"unknown or rhs type {type(rhs)}")

    def convert(
        self, func: Callable[[Optional[_Result]], _RhsResult]
    ) -> "single_results.SingleResults[_RhsResult]":
        return single_results.SingleResults[_RhsResult](func(self.value))


from pysh.core.parser.results import (
    no_results,
    single_results,
    multiple_results,
    named_results,
)
