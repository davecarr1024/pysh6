from dataclasses import dataclass, field
from typing import Callable, Iterator, Mapping, Sequence, TypeVar, Union, overload
from pysh.core.parser.results import results


_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class NamedResults(results.Results[_Result], Mapping[str, _Result]):
    _values: Mapping[str, _Result] = field(default_factory=dict[str, _Result])

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __getitem__(self, name: str) -> _Result:
        if name not in self._values:
            raise self._error(msg=f"unknown result {name}")
        return self._values[name]

    def no(self) -> "no_results.NoResults[_Result]":
        return no_results.NoResults[_Result]()

    def single(self) -> "single_results.SingleResults[_Result]":
        match len(self._values):
            case 1:
                return single_results.SingleResults[_Result](list(self.values())[0])
            case _:
                raise self._error(msg="unable to convert NamedResults to SingleResults")

    def optional(self) -> "optional_results.OptionalResults[_Result]":
        match len(self._values):
            case 0:
                return optional_results.OptionalResults[_Result]()
            case 1:
                return optional_results.OptionalResults[_Result](list(self.values())[0])
            case _:
                raise self._error(
                    msg="unable to convert NamedResults to OptionalResults"
                )

    def multiple(self) -> "multiple_results.MultipleResults[_Result]":
        return multiple_results.MultipleResults(list(self.values()))

    def named(self, name: str = "") -> "NamedResults[_Result]":
        return self

    @overload
    def __or__(
        self, rhs: "no_results.NoResults[_RhsResult]"
    ) -> "NamedResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results.SingleResults[_RhsResult]"
    ) -> "NamedResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results.OptionalResults[_RhsResult]"
    ) -> "NamedResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results.MultipleResults[_RhsResult]"
    ) -> "NamedResults[_Result|_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "NamedResults[_RhsResult]"
    ) -> "NamedResults[_Result|_RhsResult]":
        ...

    def __or__(
        self,
        rhs: Union[
            "no_results.NoResults[_RhsResult]",
            "single_results.SingleResults[_RhsResult]",
            "optional_results.OptionalResults[_RhsResult]",
            "multiple_results.MultipleResults[_RhsResult]",
            "NamedResults[_RhsResult]",
        ],
    ) -> "NamedResults[_Result | _RhsResult]":
        return NamedResults[_Result | _RhsResult](
            dict(self._values) | dict(rhs.named()._values)
        )

    def convert(
        self, func: Callable[..., _RhsResult]
    ) -> "single_results.SingleResults[_RhsResult]":
        return single_results.SingleResults[_RhsResult](func(**self))


from pysh.core.parser.results import (
    no_results,
    single_results,
    optional_results,
    multiple_results,
)
