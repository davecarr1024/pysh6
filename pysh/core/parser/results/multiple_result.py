from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized, overload

from pysh.core.parser.results import error, result, results


@dataclass(frozen=True)
class MultipleResult(results.Results[result.Result], Sized, Iterable[result.Result]):
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
                msg=f"unable to convert MultipleResult to SingleResult: invalid len {len(self)}",
            )
        else:
            return single_result.SingleResult[result.Result](self._results[0])

    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        if len(self) > 0:
            return optional_result.OptionalResult[result.Result](self._results[0])
        else:
            return optional_result.OptionalResult[result.Result]()

    def multiple(self) -> "MultipleResult[result.Result]":
        return self

    def named(
        self, name: Optional[str] = None
    ) -> "named_result.NamedResult[result.Result]":
        if len(self) > 0:
            return named_result.NamedResult[result.Result](
                {name or "": self._results[0]}
            )
        else:
            return named_result.NamedResult[result.Result]()

    @overload
    def __or__(
        self, rhs: "no_result.NoResult[result.Result]"
    ) -> "MultipleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result.SingleResult[result.Result]"
    ) -> "MultipleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result.OptionalResult[result.Result]"
    ) -> "MultipleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "MultipleResult[result.Result]"
    ) -> "MultipleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "named_result.NamedResult[result.Result]"
    ) -> "named_result.NamedResult[result.Result]":
        ...

    def __or__(
        self,
        rhs: "or_args.OrArgs",
    ) -> "results.Results[result.Result]":
        if isinstance(rhs, no_result.NoResult):
            return self
        elif isinstance(rhs, single_result.SingleResult):
            return MultipleResult(list(self) + list(rhs.multiple()))
        elif isinstance(rhs, optional_result.OptionalResult):
            return MultipleResult(list(self) + list(rhs.multiple()))
        elif isinstance(rhs, MultipleResult):
            return MultipleResult(list(self) + list(rhs))
        elif isinstance(rhs, named_result.NamedResult):
            return named_result.NamedResult(dict(self.named()) | dict(rhs))
        else:
            raise error.Error(result=self, msg="unknown results rhs {rhs}")


from pysh.core.parser.results import (
    or_args,
    no_result,
    single_result,
    optional_result,
    named_result,
)
