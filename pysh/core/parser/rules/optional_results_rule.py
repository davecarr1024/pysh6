from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import ands, rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_ConvertResult = TypeVar("_ConvertResult")
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class OptionalResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State
    ) -> states.StateAndOptionalResults[_State, _Result]:
        ...

    def convert(
        self, func: Callable[[Optional[_Result]], _ConvertResult]
    ) -> "single_results_rule.SingleResultsRule[_State,_ConvertResult]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")
        AdapterChildResult = TypeVar("AdapterChildResult")

        @dataclass(frozen=True)
        class Converter(
            single_results_rule.SingleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterChildResult],
        ):
            func: Callable[[Optional[AdapterChildResult]], AdapterResult]

            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).single().convert(self.func)

        return Converter[_State, _ConvertResult, _Result](self, func)

    @overload
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,Any]"
    ) -> "ands.OptionalResultsAnd[_State,_Result,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ands.MultipleResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "OptionalResultsRule[_State,_RhsResult]"
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
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ands.And[_State,_Result|_RhsResult, rule.Rule[_State,_Result]|rule.Rule[_State,_RhsResult]]":
        match rhs:
            case no_results_rule.NoResultsRule():
                return ands.OptionalResultsAnd[_State, _Result, _Result](
                    [
                        self,
                        no_results_unary_rule.NoResultsUnaryRule[
                            _State, _Result, _RhsResult
                        ](rhs),
                    ]
                )
            case single_results_rule.SingleResultsRule() | OptionalResultsRule() | multiple_results_rule.MultipleResultsRule():
                return ands.MultipleResultsAnd[_State, _Result, _RhsResult]([self, rhs])
            case named_results_rule.NamedResultsRule():
                return ands.NamedResultsAnd[_State, _Result, _RhsResult]([self, rhs])
            case _:
                raise self._error("invalid and rhs {rhs}")

    @overload
    def __or__(
        self, rhs: "no_results_rule.NoResultsRule[_State,Any]"
    ) -> "ors.OptionalResultsOr[_State,_Result,_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ors.OptionalResultsOr[_State,_Result,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "OptionalResultsRule[_State,_RhsResult]"
    ) -> "ors.OptionalResultsOr[_State,_Result,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ors.MultipleResultsOr[_State,_Result,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_RhsResult]"
    ) -> "ors.NamedResultsOr[_State,_Result,_RhsResult]":
        ...

    def __or__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ors.Or[_State,_Result|_RhsResult, rule.Rule[_State,_Result]|rule.Rule[_State,_RhsResult]]":
        match rhs:
            case no_results_rule.NoResultsRule():
                return ors.OptionalResultsOr[_State, _Result, _Result](
                    [
                        self,
                        no_results_unary_rule.NoResultsUnaryRule[
                            _State, _Result, _RhsResult
                        ](rhs),
                    ]
                )
            case single_results_rule.SingleResultsRule() | OptionalResultsRule():
                return ors.OptionalResultsOr[_State, _Result, _RhsResult]([self, rhs])
            case multiple_results_rule.MultipleResultsRule():
                return ors.MultipleResultsOr[_State, _Result, _RhsResult]([self, rhs])
            case named_results_rule.NamedResultsRule():
                return ors.NamedResultsOr[_State, _Result, _RhsResult]([self, rhs])
            case _:
                raise self._error("invalid or rhs {rhs}")


from pysh.core.parser.rules import (
    ands,
    ors,
    no_results_rule,
    single_results_rule,
    multiple_results_rule,
    named_results_rule,
    unary_rule,
    no_results_unary_rule,
)
