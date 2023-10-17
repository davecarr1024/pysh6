from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Self, Union, overload

from pysh.core.parser.results import result


@dataclass(frozen=True)
class Results(ABC, Generic[result.Result]):
    @overload
    @abstractmethod
    @classmethod
    def build(
        cls, rhs: "no_result.NoResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @overload
    @abstractmethod
    @classmethod
    def build(
        cls, rhs: "single_result.SingleResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @overload
    @abstractmethod
    @classmethod
    def build(
        cls, rhs: "optional_result.OptionalResult[result.Result]"
    ) -> "Results[result.Result]":
        ...

    @abstractmethod
    @classmethod
    def build(
        cls,
        rhs: Union[
            "no_result.NoResult[result.Result]",
            "single_result.SingleResult[result.Result]",
            "optional_result.OptionalResult[result.Result]",
        ],
    ) -> Self:
        ...


from pysh.core.parser.results import no_result, single_result, optional_result
