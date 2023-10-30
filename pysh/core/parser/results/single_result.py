from dataclasses import dataclass
from typing import overload

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

    @overload
    def __or__(
        self, rhs: "no_result.NoResult[result_lib.Result]"
    ) -> "SingleResult[result_lib.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "SingleResult[result_lib.Result]"
    ) -> "multiple_result.MultipleResult[result_lib.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result.OptionalResult[result_lib.Result]"
    ) -> "multiple_result.MultipleResult[result_lib.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_result.MultipleResult[result_lib.Result]"
    ) -> "multiple_result.MultipleResult[result_lib.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "named_result.NamedResult[result_lib.Result]"
    ) -> "named_result.NamedResult[result_lib.Result]":
        ...

    def __or__(
        self,
        rhs: "or_args.OrArgs",
    ) -> "results.Results[result_lib.Result]":
        if isinstance(rhs, no_result.NoResult):
            return self
        elif isinstance(rhs, SingleResult):
            return multiple_result.MultipleResult(
                list(self.multiple()) + list(rhs.multiple())
            )
        elif isinstance(rhs, optional_result.OptionalResult):
            return multiple_result.MultipleResult(
                list(self.multiple()) + list(rhs.multiple())
            )
        elif isinstance(rhs, multiple_result.MultipleResult):
            return multiple_result.MultipleResult(list(self.multiple()) + list(rhs))
        elif isinstance(rhs, named_result.NamedResult):
            return named_result.NamedResult(dict(self.named("")) | dict(rhs))
        else:
            raise error.Error(result=self, msg="unknown results rhs {rhs}")


from pysh.core.parser.results import (
    or_args,
    no_result,
    optional_result,
    multiple_result,
    named_result,
)
