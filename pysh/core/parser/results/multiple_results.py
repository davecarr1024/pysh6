from dataclasses import dataclass, field
from typing import Callable, Iterator, Sequence, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class MultipleResults(results.Results[_Result], Sequence[_Result]):
    _values: Sequence[_Result] = field(default_factory=list[_Result])

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[_Result]:
        return iter(self._values)

    @overload
    def __getitem__(self, i: int) -> _Result:
        ...

    @overload
    def __getitem__(self, i: slice) -> Sequence[_Result]:
        ...

    def __getitem__(self, i: int | slice) -> _Result | Sequence[_Result]:
        return self._values[i]

    def no(self) -> "no_results.NoResults[_Result]":
        return no_results.NoResults[_Result]()

    def single(self) -> "single_results.SingleResults[_Result]":
        match len(self._values):
            case 1:
                return single_results.SingleResults[_Result](self[0])
            case _:
                raise self._error()

    def optional(self) -> "optional_results.OptionalResults[_Result]":
        match len(self._values):
            case 0:
                return optional_results.OptionalResults[_Result]()
            case 1:
                return optional_results.OptionalResults[_Result](self[0])
            case _:
                raise self._error()

    def multiple(self) -> "MultipleResults[_Result]":
        return self

    def named(self, name: str = "") -> "named_results.NamedResults[_Result]":
        match len(self):
            case 0:
                return named_results.NamedResults[_Result]()
            case 1:
                return named_results.NamedResults[_Result]({name: self[0]})
            case _:
                raise self._error()

    @overload
    def __or__(
        self, rhs: "no_results.NoResults[_Result]"
    ) -> "MultipleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_Result]"
    ) -> "MultipleResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_Result]"
    ) -> "MultipleResults[_Result]":
        ...

    @overload
    def __or__(self, rhs: "MultipleResults[_Result]") -> "MultipleResults[_Result]":
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
            "optional_results.OptionalResults[_Result]",
            "MultipleResults[_Result]",
            "named_results.NamedResults[_Result]",
        ],
    ) -> results.Results[_Result]:
        match rhs:
            case no_results.NoResults():
                return self
            case single_results.SingleResults() | optional_results.OptionalResults():
                return self | rhs.multiple()
            case MultipleResults():
                return MultipleResults[_Result](list(self._values) + list(rhs._values))
            case named_results.NamedResults():
                return self.named() | rhs
            case _:
                raise self._error(f"unknown or rhs type {type(rhs)}")

    def convert(
        self, func: Callable[[Sequence[_Result]], _ConvertResult]
    ) -> "single_results.SingleResults[_ConvertResult]":
        return single_results.SingleResults[_ConvertResult](func(self))


from pysh.core.parser.results import (
    no_results,
    single_results,
    optional_results,
    named_results,
)
