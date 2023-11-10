from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class NamedResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndNamedResults[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,_Result]"
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_Result]"
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_Result]"
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_Result]"
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "NamedResultsRule[_State,_Result]"
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        ...

    def __and__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_Result]",
            "single_results_rule.SingleResultsRule[_State,_Result]",
            "optional_results_rule.OptionalResultsRule[_State,_Result]",
            "multiple_results_rule.MultipleResultsRule[_State,_Result]",
            "NamedResultsRule[_State,_Result]",
        ],
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        return ands.NamedResultsAnd[_State, _Result]([self, rhs])

    def convert(
        self, func: Callable[..., _ConvertResult]
    ) -> "single_results_rule.SingleResultsRule[_State,_ConvertResult]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")
        AdapterChildResult = TypeVar("AdapterChildResult")

        @dataclass(frozen=True)
        class Converter(
            single_results_rule.SingleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterChildResult],
        ):
            func: Callable[..., AdapterResult]

            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).named().convert(self.func)

        return Converter[_State, _ConvertResult, _Result](self, func)


from pysh.core.parser.rules import (
    ands,
    no_results_rule,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
    unary_rule,
)
