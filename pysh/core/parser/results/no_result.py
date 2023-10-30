from dataclasses import dataclass

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


from pysh.core.parser.results import (
    single_result,
    optional_result,
    multiple_result,
    named_result,
)
