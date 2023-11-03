from dataclasses import dataclass, field
from typing import Callable, Iterator, Mapping, Optional, overload
from pysh.core import errors
from pysh.core.parser.results import converter_result, error, result, results

NamedResultConverterFunc = Callable[..., converter_result.ConverterResult]


@dataclass(frozen=True)
class NamedResult(results.Results[result.Result], Mapping[str, result.Result]):
    _results: Mapping[str, result.Result] = field(
        default_factory=dict[str, result.Result]
    )

    def __getitem__(self, key: str) -> result.Result:
        if key not in self._results:
            raise error.Error(result=self, msg=f"unknown result {key}")
        return self._results[key]

    def __len__(self) -> int:
        return len(self._results)

    def __iter__(self) -> Iterator[str]:
        return iter(self._results)

    def no(self) -> "no_result.NoResult[result.Result]":
        return no_result.NoResult[result.Result]()

    def single(self) -> "single_result.SingleResult[result.Result]":
        if len(self) != 1:
            raise error.Error(
                result=self,
                msg=f"unable to convert NamedResult to SingleResult: invalid len {len(self)}",
            )
        else:
            return single_result.SingleResult[result.Result](
                list(self._results.values())[0]
            )

    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        if len(self) > 0:
            return optional_result.OptionalResult[result.Result](
                list(self._results.values())[0]
            )
        else:
            return optional_result.OptionalResult[result.Result]()

    def multiple(self) -> "multiple_result.MultipleResult[result.Result]":
        return multiple_result.MultipleResult[result.Result](
            list(self._results.values())
        )

    def named(self, name: Optional[str] = None) -> "NamedResult[result.Result]":
        return self

    @overload
    def __or__(
        self, rhs: "no_result.NoResult[result.Result]"
    ) -> "NamedResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result.SingleResult[result.Result]"
    ) -> "NamedResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result.OptionalResult[result.Result]"
    ) -> "NamedResult[result.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_result.MultipleResult[result.Result]"
    ) -> "multiple_result.MultipleResult[result.Result]":
        ...

    @overload
    def __or__(self, rhs: "NamedResult[result.Result]") -> "NamedResult[result.Result]":
        ...

    def __or__(
        self,
        rhs: "or_args.OrArgs",
    ) -> "results.Results[result.Result]":
        if isinstance(rhs, no_result.NoResult):
            return self
        elif isinstance(rhs, single_result.SingleResult):
            return NamedResult(dict(self) | dict(rhs.named()))
        elif isinstance(rhs, optional_result.OptionalResult):
            return NamedResult(dict(self) | dict(rhs.named()))
        elif isinstance(rhs, multiple_result.MultipleResult):
            return NamedResult(dict(self) | dict(rhs.named()))
        elif isinstance(rhs, multiple_result.MultipleResult):
            return NamedResult(dict(self) | dict(rhs))
        elif isinstance(rhs, NamedResult):
            return NamedResult(dict(self) | dict(rhs.named()))
        else:
            raise error.Error(result=self, msg="unknown results rhs {rhs}")

    def convert_type(
        self, func: NamedResultConverterFunc[converter_result.ConverterResult]
    ) -> "single_result.SingleResult[converter_result.ConverterResult]":
        try:
            return single_result.SingleResult[converter_result.ConverterResult](
                func(**dict(self))
            )
        except errors.Error as error:
            raise errors.UnaryError(child=error, msg="failed to convert NamedResult")
        except Exception as error:
            raise errors.Error(msg=f"failed ot convert NamedResult: {error}")

    def convert(
        self, func: NamedResultConverterFunc[result.Result]
    ) -> "single_result.SingleResult[result.Result]":
        try:
            return single_result.SingleResult[result.Result](func(**dict(self)))
        except errors.Error as error:
            raise errors.UnaryError(child=error, msg="failed to convert NamedResult")
        except Exception as error:
            raise errors.Error(msg=f"failed ot convert NamedResult: {error}")


from pysh.core.parser.results import (
    or_args,
    no_result,
    single_result,
    optional_result,
    multiple_result,
)
