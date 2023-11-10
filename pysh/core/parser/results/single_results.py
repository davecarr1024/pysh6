from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class SingleResults(results.Results[_Result]):
    value: _Result

    def __str__(self) -> str:
        return str(self.value)

    def no(self) -> "no_results.NoResults[_Result]":
        return no_results.NoResults[_Result]()

    def single(self) -> "SingleResults[_Result]":
        return self

    def optional(self) -> "optional_results.OptionalResults[_Result]":
        return optional_results.OptionalResults[_Result](self.value)

    def multiple(self) -> "multiple_results.MultipleResults[_Result]":
        return multiple_results.MultipleResults[_Result]([self.value])

    def named(self, name: str = "") -> "named_results.NamedResults[_Result]":
        return named_results.NamedResults[_Result]({name: self.value})

    @overload
    def __or__(
        self, rhs: "no_results.NoResults[_RhsResult]"
    ) -> "SingleResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "SingleResults[_RhsResult]"
    ) -> "multiple_results.MultipleResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_RhsResult]"
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
            "SingleResults[_RhsResult]",
            "optional_results.OptionalResults[_RhsResult]",
            "multiple_results.MultipleResults[_RhsResult]",
            "named_results.NamedResults[_RhsResult]",
        ],
    ) -> results.Results[_Result | _RhsResult]:
        match rhs:
            case no_results.NoResults():
                return SingleResults[_Result | _RhsResult](self.value)
            case SingleResults() | optional_results.OptionalResults() | multiple_results.MultipleResults():
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
        self, func: Callable[[_Result], _RhsResult]
    ) -> "SingleResults[_RhsResult]":
        return SingleResults[_RhsResult](func(self.value))


from pysh.core.parser.results import (
    no_results,
    optional_results,
    multiple_results,
    named_results,
)
