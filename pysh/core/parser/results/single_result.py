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

    def multiple(self) -> "multiple_result.MultipleResult[result_lib.Result]":
        return multiple_result.MultipleResult[result_lib.Result]([self.result])

    def named(self, name: str) -> "named_result.NamedResult[result_lib.Result]":
        return named_result.NamedResult[result_lib.Result]({name: self.result})


from pysh.core.parser.results import (
    no_result,
    optional_result,
    multiple_result,
    named_result,
)
