from dataclasses import dataclass
from typing import Callable, Optional, overload
from pysh.core.parser.results import (
    converter_result,
    error,
    result as result_lib,
    results,
)

SingleResultConverterFunc = Callable[
    [result_lib.Result], converter_result.ConverterResult
]


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

    def named(
        self, name: Optional[str] = None
    ) -> "named_result.NamedResult[result_lib.Result]":
        return named_result.NamedResult[result_lib.Result]({name or "": self.result})

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
            return multiple_result.MultipleResult[result_lib.Result](
                list(self.multiple()) + list(rhs.multiple())
            )
        elif isinstance(rhs, optional_result.OptionalResult):
            return multiple_result.MultipleResult[result_lib.Result](
                list(self.multiple()) + list(rhs.multiple())
            )
        elif isinstance(rhs, multiple_result.MultipleResult):
            return multiple_result.MultipleResult[result_lib.Result](
                list(self.multiple()) + list(rhs)
            )
        elif isinstance(rhs, named_result.NamedResult):
            return named_result.NamedResult[result_lib.Result](
                dict(self.named()) | dict(rhs)
            )
        else:
            raise error.Error(result=self, msg="unknown results rhs {rhs}")

    def convert_type(
        self,
        func: SingleResultConverterFunc[
            result_lib.Result, converter_result.ConverterResult
        ],
    ) -> "SingleResult[converter_result.ConverterResult]":
        return SingleResult[converter_result.ConverterResult](func(self.result))


from pysh.core.parser.results import (
    or_args,
    no_result,
    optional_result,
    multiple_result,
    named_result,
)
