from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


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
    def __or__(self, rhs: "no_results.NoResults[_Result]") -> "SingleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "SingleResults[_Result]"
    ) -> "multiple_results.MultipleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_Result]"
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
            "SingleResults[_Result]",
            "optional_results.OptionalResults[_Result]",
            "multiple_results.MultipleResults[_Result]",
            "named_results.NamedResults[_Result]",
        ],
    ) -> results.Results[_Result]:
        match rhs:
            case no_results.NoResults():
                return self
            case SingleResults() | optional_results.OptionalResults() | multiple_results.MultipleResults():
                return self.multiple() | rhs.multiple()
            case named_results.NamedResults():
                return self.named() | rhs
            case _:
                raise self._error(f"unknown or rhs type {type(rhs)}")

    def convert(
        self, func: Callable[[_Result], _ConvertResult]
    ) -> "SingleResults[_ConvertResult]":
        return SingleResults[_ConvertResult](func(self.value))


from pysh.core.parser.results import (
    no_results,
    optional_results,
    multiple_results,
    named_results,
)
