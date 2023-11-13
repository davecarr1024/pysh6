from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Optional, Self, Sequence, TypeVar, Union, overload
from pysh.core import errors, lexer as lexer_lib, tokens
from pysh.core.parser import results, states


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class Rule(ABC, Generic[_State, _Result]):
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
        children: Sequence[errors.Error] = [],
    ) -> errors.Error:
        @dataclass(kw_only=True, repr=False)
        class Error(errors.NaryError):
            rule: Rule
            state: _State

            def _repr_line(self) -> str:
                return f"ParseError(rule={self.rule},state={self.state},msg={repr(self.msg)})"

        return Error(rule=self, state=state, msg=msg, _children=children)

    def _error(self, msg: str) -> errors.Error:
        @dataclass(kw_only=True, repr=False)
        class Error(errors.Error):
            rule: Rule

            def _repr_line(self) -> str:
                return f"ParserRuleError(rule={self.rule},msg={repr(self.msg)})"

        return Error(rule=self, msg=msg)

    def zero_or_more(
        self,
    ) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        @dataclass(frozen=True)
        class ZeroOrMore(
            multiple_results_rule.MultipleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
        ):
            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndMultipleResults[AdapterState, AdapterResult]:
                results_ = results.MultipleResults[AdapterResult]()
                while True:
                    try:
                        child_state_and_results = self._call_child(state)
                        state = child_state_and_results.state
                        results_ |= child_state_and_results.results.multiple()
                    except errors.Error:
                        return states.StateAndMultipleResults[
                            AdapterState, AdapterResult
                        ](state, results_)

        return ZeroOrMore[_State, _Result](self)

    def one_or_more(
        self,
    ) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        @dataclass(frozen=True)
        class OneOrMore(
            multiple_results_rule.MultipleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
        ):
            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndMultipleResults[AdapterState, AdapterResult]:
                try:
                    child_state_and_results = self._call_child(state)
                    state = child_state_and_results.state
                    results_ = child_state_and_results.results.multiple()
                except errors.Error as error:
                    raise self._parse_error(state, children=[error])
                while True:
                    try:
                        child_state_and_results = self._call_child(state)
                        state = child_state_and_results.state
                        results_ |= child_state_and_results.results.multiple()
                    except errors.Error:
                        return states.StateAndMultipleResults[
                            AdapterState, AdapterResult
                        ](state, results_)

        return OneOrMore[_State, _Result](self)

    def zero_or_one(
        self,
    ) -> "optional_results_rule.OptionalResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        @dataclass(frozen=True)
        class ZeroOrOne(
            optional_results_rule.OptionalResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
        ):
            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndOptionalResults[AdapterState, AdapterResult]:
                try:
                    return self._call_child(state).optional()
                except errors.Error:
                    return states.StateAndOptionalResults[AdapterState, AdapterResult](
                        state, results.OptionalResults[AdapterResult]()
                    )

        return ZeroOrOne[_State, _Result](self)

    def no(self) -> "no_results_rule.NoResultsRule[_State,_Result]":
        return no_results_unary_rule.NoResultsUnaryRule[_State, _Result, _Result](self)

    def single(self) -> "single_results_rule.SingleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        class Adapter(
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
            single_results_rule.SingleResultsRule[AdapterState, AdapterResult],
        ):
            def __call__(
                self, state: AdapterState
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).single()

        return Adapter[_State, _Result](self)

    def optional(self) -> "optional_results_rule.OptionalResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        class Adapter(
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
            optional_results_rule.OptionalResultsRule[AdapterState, AdapterResult],
        ):
            def __call__(
                self, state: AdapterState
            ) -> states.StateAndOptionalResults[AdapterState, AdapterResult]:
                return self._call_child(state).optional()

        return Adapter[_State, _Result](self)

    def multiple(self) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        class Adapter(
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
            multiple_results_rule.MultipleResultsRule[AdapterState, AdapterResult],
        ):
            def __call__(
                self, state: AdapterState
            ) -> states.StateAndMultipleResults[AdapterState, AdapterResult]:
                return self._call_child(state).multiple()

        return Adapter[_State, _Result](self)

    def named(
        self, name: str = ""
    ) -> "named_results_rule.NamedResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        class Adapter(
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
            named_results_rule.NamedResultsRule[AdapterState, AdapterResult],
        ):
            def __call__(
                self, state: AdapterState
            ) -> states.StateAndNamedResults[AdapterState, AdapterResult]:
                return self._call_child(state).named(name)

        return Adapter[_State, _Result](self)

    def until(
        self,
        term_rule: Union[
            "no_results_rule.NoResultsRule[_State,Any]",
            lexer_lib.Rule,
            str,
        ],
    ) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        match term_rule:
            case str() | lexer_lib.Rule():
                term_rule = literal.Literal[_State].load(term_rule).no()

        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        @dataclass(frozen=True)
        class Adapter(
            multiple_results_rule.MultipleResultsRule[AdapterState, AdapterResult],
        ):
            iter_rule: Rule[AdapterState, AdapterResult]
            term_rule: Rule[AdapterState, Any]

            def lexer(self) -> lexer_lib.Lexer:
                return self.iter_rule.lexer() | self.term_rule.lexer()

            def __call__(
                self, state: AdapterState
            ) -> states.StateAndMultipleResults[AdapterState, AdapterResult]:
                results_ = results.MultipleResults[AdapterResult]()
                while True:
                    try:
                        return states.StateAndMultipleResults[
                            AdapterState, AdapterResult
                        ](self.term_rule(state).state, results_)
                    except errors.Error as error:
                        term_error = error
                    try:
                        child_results_and_state = self.iter_rule(state)
                        results_ |= child_results_and_state.results.multiple()
                        state = child_results_and_state.state
                    except errors.Error as error:
                        raise self._parse_error(state, children=[term_error])

        return Adapter[_State, _Result](self, term_rule)

    def until_empty(
        self,
    ) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState", bound=states.State)
        AdapterResult = TypeVar("AdapterResult")

        @dataclass(frozen=True)
        class Adapter(
            multiple_results_rule.MultipleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[AdapterState, AdapterResult, AdapterResult],
        ):
            def __call__(
                self, state: AdapterState
            ) -> states.StateAndMultipleResults[AdapterState, AdapterResult]:
                results_ = results.MultipleResults[AdapterResult]()
                while state.lexer_result.tokens:
                    child_state_and_results = self._call_child(state).multiple()
                    state = child_state_and_results.state
                    results_ |= child_state_and_results.results
                return states.StateAndMultipleResults[AdapterState, AdapterResult](
                    state, results_
                )

        return Adapter[_State, _Result](self)

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
    unary_rule,
    no_results_unary_rule,
    literal,
)
