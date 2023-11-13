from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, TypeVar, Union, overload
from pysh.core import lexer as lexer_lib
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_ConvertResult = TypeVar("_ConvertResult")
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class NamedResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndNamedResults[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,Any]"
    ) -> "ands.NamedResultsAnd[_State,_Result,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ands.NamedResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> "ands.NamedResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ands.NamedResultsAnd[_State,_Result,_RhsResult]":
        ...

    @overload
    def __and__(
        self, rhs: "NamedResultsRule[_State,_RhsResult]"
    ) -> "ands.NamedResultsAnd[_State,_Result,_RhsResult]":
        ...

    def __and__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ands.And[_State,_Result|_RhsResult, rule.Rule[_State,_Result]|rule.Rule[_State,_RhsResult]]":
        match rhs:
            case no_results_rule.NoResultsRule():
                return ands.NamedResultsAnd[_State, _Result, _Result](
                    [
                        self,
                        no_results_unary_rule.NoResultsUnaryRule[
                            _State, _Result, _RhsResult
                        ](rhs),
                    ]
                )
            case _:
                return ands.NamedResultsAnd[_State, _Result, _RhsResult]([self, rhs])

    def convert(
        self, func: Callable[..., _ConvertResult]
    ) -> "single_results_rule.SingleResultsRule[_State,_ConvertResult]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
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

    @overload
    def __or__(
        self, rhs: "no_results_rule.NoResultsRule[_State,Any]"
    ) -> "ors.NamedResultsOr[_State,_Result,_Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ors.NamedResultsOr[_State,_Result,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> "ors.NamedResultsOr[_State,_Result,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ors.NamedResultsOr[_State,_Result,_RhsResult]":
        ...

    @overload
    def __or__(
        self, rhs: "NamedResultsRule[_State,_RhsResult]"
    ) -> "ors.NamedResultsOr[_State,_Result,_RhsResult]":
        ...

    def __or__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> "ors.Or[_State,_Result|_RhsResult, rule.Rule[_State,_Result]|rule.Rule[_State,_RhsResult]]":
        match rhs:
            case no_results_rule.NoResultsRule():
                return ors.NamedResultsOr[_State, _Result, _Result](
                    [
                        self,
                        no_results_unary_rule.NoResultsUnaryRule[
                            _State, _Result, _RhsResult
                        ](rhs),
                    ]
                )
            case _:
                return ors.NamedResultsOr[_State, _Result, _RhsResult]([self, rhs])

    def with_lexer(self, lexer: lexer_lib.Lexer) -> "NamedResultsRule[_State,_Result]":
        State = TypeVar("State", bound=states.State)
        Result = TypeVar("Result")

        @dataclass(frozen=True)
        class WithLexer(
            unary_rule.UnaryRule[State, Result, Result],
            NamedResultsRule[State, Result],
        ):
            _lexer: lexer_lib.Lexer

            def lexer(self) -> lexer_lib.Lexer:
                return self._lexer | self.child.lexer()

            def __call__(
                self, state: State
            ) -> states.StateAndNamedResults[State, Result]:
                return self._call_child(state).named()

        return WithLexer[_State, _Result](child=self, _lexer=lexer)


from pysh.core.parser.rules import (
    ands,
    ors,
    no_results_rule,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
    unary_rule,
    no_results_unary_rule,
)
