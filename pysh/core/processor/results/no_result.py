from dataclasses import dataclass

from pysh.core.processor.results import error, result, results


@dataclass(frozen=True)
class NoResult(results.Results[result.Result]):
    def no(self) -> "NoResult[result.Result]":
        return self

    def single(self) -> "single_result.SingleResult[result.Result]":
        raise error.Error(result=self, msg="unable to convert NoResult to SingleResult")

    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        return optional_result.OptionalResult[result.Result]()

    def multiple(self) -> "multiple_results.MultipleResults[result.Result]":
        return multiple_results.MultipleResults[result.Result]()

    def named(self, name: str) -> "named_results.NamedResults[result.Result]":
        return named_results.NamedResults[result.Result]()


from pysh.core.processor.results import (
    single_result,
    optional_result,
    multiple_results,
    named_results,
)
