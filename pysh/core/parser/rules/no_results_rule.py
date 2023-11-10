from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


@dataclass(frozen=True)
class NoResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndNoResults[_State, _Result]:
        ...

    def convert(
        self, func: Callable[[], _ConvertResult]
    ) -> "single_results_rule.SingleResultsRule[_State,_ConvertResult]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")
        AdapterChildResult = TypeVar("AdapterChildResult")

        @dataclass(frozen=True)
        class Converter(
            single_results_rule.SingleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterChildResult],
        ):
            func: Callable[[], AdapterResult]

            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).no().convert(self.func)

        return Converter[_State, _ConvertResult, _Result](self, func)

    @overload
    def __and__(
        self, rhs: "NoResultsRule[_State,_Result]"
    ) -> "ands.NoResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_Result]"
    ) -> "ands.SingleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_Result]"
    ) -> "ands.OptionalResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_Result]"
    ) -> "ands.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_Result]"
    ) -> "ands.NamedResultsAnd[_State,_Result]":
        ...

    def __and__(
        self,
        rhs: Union[
            "NoResultsRule[_State,_Result]",
            "single_results_rule.SingleResultsRule[_State,_Result]",
            "optional_results_rule.OptionalResultsRule[_State,_Result]",
            "multiple_results_rule.MultipleResultsRule[_State,_Result]",
            "named_results_rule.NamedResultsRule[_State,_Result]",
        ],
    ) -> "ands.And[_State,_Result, rule.Rule[_State,_Result]]":
        match rhs:
            case NoResultsRule():
                return ands.NoResultsAnd[_State, _Result]([self, rhs])
            case single_results_rule.SingleResultsRule():
                return ands.SingleResultsAnd[_State, _Result]([self, rhs])
            case optional_results_rule.OptionalResultsRule():
                return ands.OptionalResultsAnd[_State, _Result]([self, rhs])
            case multiple_results_rule.MultipleResultsRule():
                return ands.MultipleResultsAnd[_State, _Result]([self, rhs])
            case named_results_rule.NamedResultsRule():
                return ands.NamedResultsAnd[_State, _Result]([self, rhs])
            case _:
                raise self._error("invalid and rhs {rhs}")


from pysh.core.parser.rules import (
    ands,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
    named_results_rule,
    unary_rule,
)
