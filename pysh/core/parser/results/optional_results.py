from dataclasses import dataclass
from typing import Callable, Optional, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


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
        self, rhs: "no_results.NoResults[_Result]"
    ) -> "OptionalResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_Result]"
    ) -> "multiple_results.MultipleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "OptionalResults[_Result]"
    ) -> "multiple_results.MultipleResults[_Result]":
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
            "no_results.NoResults[_Result]",
            "single_results.SingleResults[_Result]",
            "OptionalResults[_Result]",
            "multiple_results.MultipleResults[_Result]",
            "named_results.NamedResults[_Result]",
        ],
    ) -> results.Results[_Result]:
        match rhs:
            case no_results.NoResults():
                return self
            case single_results.SingleResults() | OptionalResults() | multiple_results.MultipleResults():
                return self.multiple() | rhs.multiple()
            case named_results.NamedResults():
                return self.named() | rhs
            case _:
                raise self._error(f"unknown or rhs type {type(rhs)}")

    def convert(
        self, func: Callable[[Optional[_Result]], _ConvertResult]
    ) -> "single_results.SingleResults[_ConvertResult]":
        return single_results.SingleResults[_ConvertResult](func(self.value))


from pysh.core.parser.results import (
    no_results,
    single_results,
    multiple_results,
    named_results,
)
