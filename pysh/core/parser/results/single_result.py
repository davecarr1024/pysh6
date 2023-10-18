from dataclasses import dataclass

from pysh.core.parser.results import error, result as result_lib, results


@dataclass(frozen=True)
class SingleResult(results.Results[result_lib.Result]):
    result: result_lib.Result

    def no(self) -> "no_result.NoResult[result_lib.Result]":
        return no_result.NoResult[result_lib.Result]()

    def single(self) -> "SingleResult[result_lib.Result]":
        return self

    def optional(self) -> "optional_result.OptionalResult[result_lib.Result]":
        return optional_result.OptionalResult[result_lib.Result](self.result)

    def multiple(self) -> "multiple_results.MultipleResults[result_lib.Result]":
        return multiple_results.MultipleResults[result_lib.Result]([self.result])

    def named(self, name: str) -> "named_results.NamedResults[result_lib.Result]":
        return named_results.NamedResults[result_lib.Result]({name: self.result})


from pysh.core.parser.results import (
    no_result,
    optional_result,
    multiple_results,
    named_results,
)
