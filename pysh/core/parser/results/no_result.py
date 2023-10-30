from dataclasses import dataclass
from typing import overload

from pysh.core.parser.results import error, result, results


@dataclass(frozen=True)
class NoResult(results.Results[result.Result]):
    def no(self) -> "NoResult[result.Result]":
        return self

    def single(self) -> "single_result.SingleResult[result.Result]":
        raise error.Error(result=self, msg="unable to convert NoResult to SingleResult")

    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        return optional_result.OptionalResult[result.Result]()

    def multiple(self) -> "multiple_result.MultipleResult[result.Result]":
        return multiple_result.MultipleResult[result.Result]()

    def named(self, name: str) -> "named_result.NamedResult[result.Result]":
        return named_result.NamedResult[result.Result]()

    @overload
    def __or__(
        self, rhs: "NoResult[result.Result]"
    ) -> "single_result.SingleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result.SingleResult[result.Result]"
    ) -> "multiple_result.MultipleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result.OptionalResult[result.Result]"
    ) -> "multiple_result.MultipleResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_result.MultipleResult[result.Result]"
    ) -> "multiple_result.MultipleResult[result.Result]":
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
        return rhs


from pysh.core.parser.results import (
    or_args,
    single_result,
    optional_result,
    multiple_result,
    named_result,
)
