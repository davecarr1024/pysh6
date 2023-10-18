from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic

from pysh.core.processor.results import result


@dataclass(frozen=True)
class Results(ABC, Generic[result.Result]):
    @abstractmethod
    def no(self) -> "no_result.NoResult[result.Result]":
        ...

    @abstractmethod
    def single(self) -> "single_result.SingleResult[result.Result]":
        ...

    @abstractmethod
    def optional(self) -> "optional_result.OptionalResult[result.Result]":
        ...

    @abstractmethod
    def multiple(self) -> "multiple_results.MultipleResults[result.Result]":
        ...

    @abstractmethod
    def named(self, name: str) -> "named_results.NamedResults[result.Result]":
        ...


from pysh.core.processor.results import (
    no_result,
    single_result,
    optional_result,
    multiple_results,
    named_results,
)
