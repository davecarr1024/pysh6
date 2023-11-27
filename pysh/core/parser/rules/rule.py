from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Optional, Self, Sequence, TypeVar, Union, overload
from pysh.core import errors, lexer as lexer_lib, tokens
from pysh.core.parser import results, states


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class Rule(
    ABC,
    Generic[_State, _Result],
    errors.Errorable["Rule"],
):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndResults[_State, _Result]:
        ...

    def lexer(self) -> lexer_lib.Lexer:
        return lexer_lib.Lexer()

    def _parse_error(
        self,
        state: _State,
        *,
        msg: Optional[str] = None,
        children: Optional[Sequence[errors.Error]] = None,
    ) -> errors.Error:
        return self._error(state=state, msg=msg, children=children or [])

    def zero_or_more(
        self,
    ) -> "unary_rules.ZeroOrMore[_State,_Result]":
        return unary_rules.ZeroOrMore[_State, _Result](self)

    def one_or_more(
        self,
    ) -> "unary_rules.OneOrMore[_State,_Result]":
        return unary_rules.OneOrMore[_State, _Result](self)

    def zero_or_one(
        self,
    ) -> "unary_rules.ZeroOrOne[_State,_Result]":
        return unary_rules.ZeroOrOne[_State, _Result](self)

    def no(self) -> "unary_rules.NoResultsUnaryRule[_State,_Result,_Result]":
        return unary_rules.NoResultsUnaryRule[_State, _Result, _Result](self)

    def single(self) -> "unary_rules.SingleResultsUnaryRule[_State,_Result]":
        return unary_rules.SingleResultsUnaryRule[_State, _Result](self)

    def optional(self) -> "unary_rules.OptionalResultsUnaryRule[_State,_Result]":
        return unary_rules.OptionalResultsUnaryRule[_State, _Result](self)

    def multiple(self) -> "unary_rules.MultipleResultsUnaryRule[_State,_Result]":
        return unary_rules.MultipleResultsUnaryRule[_State, _Result](self)

    def named(
        self, name: str = ""
    ) -> "unary_rules.NamedResultsUnaryRule[_State,_Result]":
        return unary_rules.NamedResultsUnaryRule[_State, _Result](self, name)

    def until(
        self,
        term_rule: Union[
            "no_results_rule.NoResultsRule[_State,Any]",
            lexer_lib.Rule,
            str,
        ],
    ) -> "unary_rules.Until[_State,_Result]":
        match term_rule:
            case str() | lexer_lib.Rule():
                term_rule = literal.Literal[_State].load(term_rule).no()

        return unary_rules.Until[_State, _Result](self, term_rule)

    def until_empty(
        self,
    ) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        return unary_rules.UntilEmpty[_State, _Result](self)

    @abstractmethod
    def with_lexer(self, lexer: lexer_lib.Lexer) -> Self:
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,_RhsResult]"
    ) -> "ands.And[_State,_Result|_RhsResult, Rule[_State,_Result]|Rule[_State,_RhsResult]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> "ands.And[_State,_Result|_RhsResult, Rule[_State,_Result]|Rule[_State,_RhsResult]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> "ands.And[_State,_Result|_RhsResult, Rule[_State,_Result]|Rule[_State,_RhsResult]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> "ands.And[_State,_Result|_RhsResult, Rule[_State,_Result]|Rule[_State,_RhsResult]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_RhsResult]"
    ) -> "ands.And[_State,_Result|_RhsResult, Rule[_State,_Result]|Rule[_State,_RhsResult]]":
        ...

    @overload
    @abstractmethod
    def __and__(self, rhs: str) -> "ands.And[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: lexer_lib.Rule
    ) -> "ands.And[_State,_Result,Rule[_State,_Result]]":
        ...

    @abstractmethod
    def __and__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
            lexer_lib.Rule,
            str,
        ],
    ) -> "ands.And[_State,_Result|_RhsResult, Rule[_State,_Result]|Rule[_State,_RhsResult]]":
        ...

    @overload
    @abstractmethod
    def __rand__(self, rhs: str) -> "ands.And[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __rand__(
        self, rhs: lexer_lib.Rule
    ) -> "ands.And[_State,_Result,Rule[_State,_Result]]":
        ...

    @abstractmethod
    def __rand__(
        self,
        rhs: Union[
            str,
            lexer_lib.Rule,
        ],
    ) -> "ands.And[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "no_results_rule.NoResultsRule[_State,_RhsResult]"
    ) -> (
        "ors.Or[_State,_Result|_RhsResult,Rule[_State,_Result]|Rule[_State,_RhsResult]]"
    ):
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_RhsResult]"
    ) -> (
        "ors.Or[_State,_Result|_RhsResult,Rule[_State,_Result]|Rule[_State,_RhsResult]]"
    ):
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_RhsResult]"
    ) -> (
        "ors.Or[_State,_Result|_RhsResult,Rule[_State,_Result]|Rule[_State,_RhsResult]]"
    ):
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]"
    ) -> (
        "ors.Or[_State,_Result|_RhsResult,Rule[_State,_Result]|Rule[_State,_RhsResult]]"
    ):
        ...

    @overload
    @abstractmethod
    def __or__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_RhsResult]"
    ) -> (
        "ors.Or[_State,_Result|_RhsResult,Rule[_State,_Result]|Rule[_State,_RhsResult]]"
    ):
        ...

    @abstractmethod
    def __or__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_RhsResult]",
            "single_results_rule.SingleResultsRule[_State,_RhsResult]",
            "optional_results_rule.OptionalResultsRule[_State,_RhsResult]",
            "multiple_results_rule.MultipleResultsRule[_State,_RhsResult]",
            "named_results_rule.NamedResultsRule[_State,_RhsResult]",
        ],
    ) -> (
        "ors.Or[_State,_Result|_RhsResult,Rule[_State,_Result]|Rule[_State,_RhsResult]]"
    ):
        ...


from pysh.core.parser.rules import (
    ands,
    ors,
    no_results_rule,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
    named_results_rule,
    literal,
    unary_rules,
)
