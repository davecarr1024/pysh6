from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core import lexer as lexer_lib
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_ConvertResult = TypeVar("_ConvertResult")
_RhsResult = TypeVar("_RhsResult")


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
        self, rhs: "NoResultsRule[_State,_RhsResult]"
    ) -> "ands.NoResultsAnd[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ands.SingleResultsAnd[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> "ands.OptionalResultsAnd[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ands.MultipleResultsAnd[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_RhsResult]"
    ) -> "ands.NamedResultsAnd[_State,_RhsResult,_RhsResult]":
        ...

    def __and__(
        self,
        rhs: Union[
            "NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ands.And[_State,_RhsResult, rule.Rule[_State,_RhsResult]]":
        rhs_result_self = no_results_unary_rule.NoResultsUnaryRule[
            _State, _RhsResult, _Result
        ](self)
        match rhs:
            case NoResultsRule():
                return ands.NoResultsAnd[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case single_results_rule.SingleResultsRule():
                return ands.SingleResultsAnd[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case optional_results_rule.OptionalResultsRule():
                return ands.OptionalResultsAnd[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case multiple_results_rule.MultipleResultsRule():
                return ands.MultipleResultsAnd[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case named_results_rule.NamedResultsRule():
                return ands.NamedResultsAnd[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case _:
                raise self._error("invalid and rhs {rhs}")

    @overload
    def __or__(
        self, rhs: "NoResultsRule[_State,_RhsResult]"
    ) -> "ors.NoResultsOr[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ors.SingleResultsOr[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> "ors.OptionalResultsOr[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ors.MultipleResultsOr[_State,_RhsResult,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_RhsResult]"
    ) -> "ors.NamedResultsOr[_State,_RhsResult,_RhsResult]":
        ...

    def __or__(
        self,
        rhs: Union[
            "NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ors.Or[_State,_RhsResult, rule.Rule[_State,_RhsResult]]":
        rhs_result_self = no_results_unary_rule.NoResultsUnaryRule[
            _State, _RhsResult, _Result
        ](self)
        match rhs:
            case NoResultsRule():
                return ors.NoResultsOr[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case single_results_rule.SingleResultsRule():
                return ors.OptionalResultsOr[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case optional_results_rule.OptionalResultsRule():
                return ors.OptionalResultsOr[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case multiple_results_rule.MultipleResultsRule():
                return ors.MultipleResultsOr[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case named_results_rule.NamedResultsRule():
                return ors.NamedResultsOr[_State, _RhsResult, _RhsResult](
                    [rhs_result_self, rhs]
                )
            case _:
                raise self._error("invalid or rhs {rhs}")

    def with_lexer(self, lexer: lexer_lib.Lexer) -> "NoResultsRule[_State,_Result]":
        State = TypeVar("State")
        Result = TypeVar("Result")

        @dataclass(frozen=True)
        class WithLexer(
            unary_rule.UnaryRule[State, Result, Result],
            NoResultsRule[State, Result],
        ):
            _lexer: lexer_lib.Lexer

            def lexer(self) -> lexer_lib.Lexer:
                return self._lexer | self.child.lexer()

            def __call__(self, state: State) -> states.StateAndNoResults[State, Result]:
                return self._call_child(state).no()

        return WithLexer[_State, _Result](child=self, _lexer=lexer)


from pysh.core.parser.rules import (
    ands,
    ors,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
    named_results_rule,
    unary_rule,
    no_results_unary_rule,
)
