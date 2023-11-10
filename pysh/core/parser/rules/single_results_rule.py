from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_ConvertResult = TypeVar("_ConvertResult")
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class SingleResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        ...

    def convert(
        self, func: Callable[[_Result], _ConvertResult]
    ) -> "SingleResultsRule[_State,_ConvertResult]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")
        AdapterChildResult = TypeVar("AdapterChildResult")

        @dataclass(frozen=True)
        class Converter(
            SingleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterChildResult],
        ):
            func: Callable[[AdapterChildResult], AdapterResult]

            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).single().convert(self.func)

        return Converter[_State, _ConvertResult, _Result](self, func)

    @overload
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,_RhsResult]"
    ) -> "ands.SingleResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultsRule[_State,_RhsResult]"
    ) -> "ands.MultipleResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> "ands.MultipleResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ands.MultipleResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_RhsResult]"
    ) -> "ands.NamedResultsAnd[_State,_Result,_RhsResult]":
        ...

    def __and__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_RhsResult]",
            "SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ands.And[_State,_Result|_RhsResult, rule.Rule[_State,_Result]|rule.Rule[_State,_RhsResult]]":
        match rhs:
            case no_results_rule.NoResultsRule():
                return ands.SingleResultsAnd[_State, _Result, _RhsResult]([self, rhs])
            case SingleResultsRule() | optional_results_rule.OptionalResultsRule() | multiple_results_rule.MultipleResultsRule():
                return ands.MultipleResultsAnd[_State, _Result, _RhsResult]([self, rhs])
            case named_results_rule.NamedResultsRule():
                return ands.NamedResultsAnd[_State, _Result, _RhsResult]([self, rhs])
            case _:
                raise self._error("invalid and rhs {rhs}")


from pysh.core.parser.rules import (
    ands,
    unary_rule,
    no_results_rule,
    optional_results_rule,
    multiple_results_rule,
    named_results_rule,
)
