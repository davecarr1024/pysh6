from dataclasses import dataclass, field
from typing import Callable, Iterator, Mapping, Sequence, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class NamedResults(results.Results[_Result], Mapping[str, _Result]):
    _values: Mapping[str, _Result] = field(default_factory=dict[str, _Result])

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __getitem__(self, name: str) -> _Result:
        if name not in self._values:
            raise self._error(f"unknown result {name}")
        return self._values[name]

    def no(self) -> "no_results.NoResults[_Result]":
        return no_results.NoResults[_Result]()

    def single(self) -> "single_results.SingleResults[_Result]":
        match len(self._values):
            case 1:
                return single_results.SingleResults[_Result](list(self.values())[0])
            case _:
                raise self._error()

    def optional(self) -> "optional_results.OptionalResults[_Result]":
        match len(self._values):
            case 0:
                return optional_results.OptionalResults[_Result]()
            case 1:
                return optional_results.OptionalResults[_Result](list(self.values())[0])
            case _:
                raise self._error()

    def multiple(self) -> "multiple_results.MultipleResults[_Result]":
        return multiple_results.MultipleResults(list(self.values()))

    def named(self, name: str = "") -> "NamedResults[_Result]":
        return self

    @overload
    def __or__(self, rhs: "no_results.NoResults[_Result]") -> "NamedResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_Result]"
    ) -> "NamedResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_Result]"
    ) -> "NamedResults[_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results.MultipleResults[_Result]"
    ) -> "NamedResults[_Result]":
        ...

    @overload
    def __or__(self, rhs: "NamedResults[_Result]") -> "NamedResults[_Result]":
        ...

    def __or__(
        self,
        rhs: Union[
            "no_results.NoResults[_Result]",
            "single_results.SingleResults[_Result]",
            "optional_results.OptionalResults[_Result]",
            "multiple_results.MultipleResults[_Result]",
            "NamedResults[_Result]",
        ],
    ) -> results.Results[_Result]:
        match rhs:
            case no_results.NoResults():
                return self
            case single_results.SingleResults() | optional_results.OptionalResults() | multiple_results.MultipleResults():
                return self | rhs.named()
            case NamedResults():
                return NamedResults[_Result](dict(self._values) | dict(rhs._values))
            case _:
                raise self._error(f"unknown or rhs type {type(rhs)}")

    def convert(
        self, func: Callable[..., _ConvertResult]
    ) -> "single_results.SingleResults[_ConvertResult]":
        return single_results.SingleResults[_ConvertResult](func(**self))


from pysh.core.parser.results import (
    no_results,
    single_results,
    optional_results,
    multiple_results,
)
