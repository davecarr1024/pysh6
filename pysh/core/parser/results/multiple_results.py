from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized

from pysh.core.parser.results import error, result, results


@dataclass(frozen=True)
class MultipleResults(results.Results[result.Result], Sized, Iterable[result.Result]):
    _results: Sequence[result.Result] = field(default_factory=list[result.Result])

    def __len__(self) -> int:
        return len(self._results)

    def __iter__(self) -> Iterator[result.Result]:
        return iter(self._results)

    def no(self) -> "no_result.NoResult[result.Result]":
        return no_result.NoResult[result.Result]()

    def single(self) -> "single_result.SingleResult[result.Result]":
        if len(self) != 1:
            raise error.Error(
                result=self,
                msg=f"unable to convert MultipleResults to SingleResult: invalid len {len(self)}",
            )
        else:
            return single_result.SingleResult[result.Result](self._results[0])

    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        if len(self) > 1:
            raise error.Error(
                result=self,
                msg=f"unable to convert MultipleResults to OptionalResult: invalid len {len(self)}",
            )
        elif len(self) == 0:
            return optional_result.OptionalResult[result.Result]()
        else:
            return optional_result.OptionalResult[result.Result](self._results[0])

    def multiple(self) -> "MultipleResults[result.Result]":
        return self

    def named(self, name: str) -> "named_results.NamedResults[result.Result]":
        if len(self) > 1:
            raise error.Error(
                result=self,
                msg=f"unable to convert MultipleResults to NamedResults: invalid len {len(self)}",
            )
        elif len(self) == 1:
            return named_results.NamedResults[result.Result]({name: self._results[0]})
        else:
            return named_results.NamedResults[result.Result]()


from pysh.core.parser.results import (
    no_result,
    single_result,
    optional_result,
    named_results,
)
