from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core import lexer as lexer_lib, tokens
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State", bound=states.State)
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
        return unary_rules.NoResultsConverter[_State, _ConvertResult, _Result](
            self, func
        )

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

    @overload
    def __and__(self, rhs: str) -> "ands.NoResultsAnd[_State,_Result,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: lexer_lib.Rule
    ) -> "ands.NoResultsAnd[_State,_Result,_Result]":
        ...

    def __and__(
        self,
        rhs: Union[
            "NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
            lexer_lib.Rule,
            str,
        ],
    ) -> "ands.And[_State,_Result|_RhsResult, rule.Rule[_State,_Result]|rule.Rule[_State,_RhsResult]]":
        rhs_result_self = unary_rules.NoResultsUnaryRule[_State, _RhsResult, _Result](
            self
        )
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
            case str() | lexer_lib.Rule():
                return ands.NoResultsAnd[_State, _Result, _Result](
                    [
                        self,
                        unary_rules.NoResultsUnaryRule[_State, _Result, tokens.Token](
                            literal.Literal[_State].load(rhs)
                        ),
                    ]
                )
            case _:
                raise self._error(msg="invalid and rhs {rhs}")

    @overload
    def __rand__(self, rhs: str) -> "ands.NoResultsAnd[_State, _Result, _Result]":
        ...

    @overload
    def __rand__(
        self, rhs: lexer_lib.Rule
    ) -> "ands.NoResultsAnd[_State, _Result, _Result]":
        ...

    def __rand__(
        self,
        rhs: Union[
            str,
            lexer_lib.Rule,
        ],
    ) -> "ands.NoResultsAnd[_State, _Result, _Result]":
        return ands.NoResultsAnd[_State, _Result, _Result](
            [
                unary_rules.NoResultsUnaryRule[_State, _Result, tokens.Token](
                    literal.Literal.load(rhs)
                ),
                self,
            ]
        )

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
        rhs_result_self = unary_rules.NoResultsUnaryRule[_State, _RhsResult, _Result](
            self
        )
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
                raise self._error(msg=f"invalid or rhs {rhs}")

    def with_lexer(self, lexer: lexer_lib.Lexer) -> "NoResultsRule[_State,_Result]":
        return unary_rules.NoResultsUnaryRule[
            _State,
            _Result,
            _Result,
        ](
            self,
            _lexer=lexer,
        )


from pysh.core.parser.rules import (
    ands,
    ors,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
    named_results_rule,
    literal,
    unary_rules,
)
