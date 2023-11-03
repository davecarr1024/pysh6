from dataclasses import dataclass
from typing import Callable, Optional, overload
from pysh.core.parser.results import (
    converter_result,
    error,
    result as result_lib,
    results,
)

OptionalResultConverterFunc = Callable[
    [Optional[result_lib.Result]], converter_result.ConverterResult
]


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

    def named(
        self, name: Optional[str] = None
    ) -> "named_result.NamedResult[result_lib.Result]":
        if self.result is None:
            return named_result.NamedResult[result_lib.Result]()
        else:
            return named_result.NamedResult[result_lib.Result](
                {name or "": self.result}
            )

    @overload
    def __or__(
        self, rhs: "no_result.NoResult[result_lib.Result]"
    ) -> "OptionalResult[result_lib.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result.SingleResult[result_lib.Result]"
    ) -> "multiple_result.MultipleResult[result_lib.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "OptionalResult[result_lib.Result]"
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
        elif isinstance(rhs, single_result.SingleResult):
            return multiple_result.MultipleResult[result_lib.Result](
                list(self.multiple()) + list(rhs.multiple())
            )
        elif isinstance(rhs, OptionalResult):
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
        func: OptionalResultConverterFunc[
            result_lib.Result, converter_result.ConverterResult
        ],
    ) -> "single_result.SingleResult[converter_result.ConverterResult]":
        return single_result.SingleResult[converter_result.ConverterResult](
            func(self.result)
        )

    def convert(
        self, func: OptionalResultConverterFunc[result_lib.Result, result_lib.Result]
    ) -> "single_result.SingleResult[result_lib.Result]":
        return single_result.SingleResult[result_lib.Result](func(self.result))


from pysh.core.parser.results import (
    or_args,
    no_result,
    single_result,
    multiple_result,
    named_result,
)
