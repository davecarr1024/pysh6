from dataclasses import dataclass
from typing import Optional

from pysh.core.parser.results import error, result as result_lib, results


@dataclass(frozen=True)
class OptionalResult(results.Results[result_lib.Result]):
    result: Optional[result_lib.Result] = None

    def no(self) -> "no_result.NoResult[result_lib.Result]":
        return no_result.NoResult[result_lib.Result]()

    def single(self) -> "single_result.SingleResult[result_lib.Result]":
        if self.result is None:
            raise error.Error(
                result=self,
                msg="unable to convert OptionalResult to SingleResult: no result",
            )
        return single_result.SingleResult[result_lib.Result](self.result)

    def optional(self) -> "OptionalResult[result_lib.Result]":
        return self

    def multiple(self) -> "multiple_result.MultipleResult[result_lib.Result]":
        if self.result is None:
            return multiple_result.MultipleResult[result_lib.Result]()
        else:
            return multiple_result.MultipleResult[result_lib.Result]([self.result])

    def named(self, name: str) -> "named_result.NamedResult[result_lib.Result]":
        if self.result is None:
            return named_result.NamedResult[result_lib.Result]()
        else:
            return named_result.NamedResult[result_lib.Result]({name: self.result})


from pysh.core.parser.results import (
    no_result,
    single_result,
    multiple_result,
    named_result,
)
