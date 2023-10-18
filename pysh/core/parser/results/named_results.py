from dataclasses import dataclass, field
from typing import Iterator, Mapping

from pysh.core.parser.results import error, result, results


@dataclass(frozen=True)
class NamedResults(results.Results[result.Result], Mapping[str, result.Result]):
    _results: Mapping[str, result.Result] = field(
        default_factory=dict[str, result.Result]
    )

    def __getitem__(self, key: str) -> result.Result:
        if key not in self._results:
            raise error.Error(result=self, msg=f"unknown result {key}")
        return self._results[key]

    def __len__(self) -> int:
        return len(self._results)

    def __iter__(self) -> Iterator[str]:
        return iter(self._results)

    def no(self) -> "no_result.NoResult[result.Result]":
        return no_result.NoResult[result.Result]()

    def single(self) -> "single_result.SingleResult[result.Result]":
        if len(self) != 1:
            raise error.Error(
                result=self,
                msg=f"unable to convert NamedResult to SingleResult: invalid len {len(self)}",
            )
        else:
            return single_result.SingleResult[result.Result](
                list(self._results.values())[0]
            )

    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        if len(self) > 1:
            raise error.Error(
                result=self,
                msg=f"unable to convert NamedResult to SingleResult: invalid len {len(self)}",
            )
        elif len(self) == 1:
            return optional_result.OptionalResult[result.Result](
                list(self._results.values())[0]
            )
        else:
            return optional_result.OptionalResult[result.Result]()

    def multiple(self) -> "multiple_results.MultipleResults[result.Result]":
        return multiple_results.MultipleResults[result.Result](
            list(self._results.values())
        )

    def named(self, name: str) -> "NamedResults[result.Result]":
        return self


from pysh.core.parser.results import (
    no_result,
    single_result,
    optional_result,
    multiple_results,
)
