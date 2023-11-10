from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class MultipleResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State
    ) -> states.StateAndMultipleResults[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,_Result]"
    ) -> "multiple_results_and.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_Result]"
    ) -> "multiple_results_and.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_Result]"
    ) -> "multiple_results_and.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "MultipleResultsRule[_State,_Result]"
    ) -> "multiple_results_and.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "named_results_rule.NamedResultsRule[_State,_Result]"
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
        ...

    def __and__(
        self,
        rhs: Union[
            "no_results_rule.NoResultsRule[_State,_Result]",
            "single_results_rule.SingleResultsRule[_State,_Result]",
            "optional_results_rule.OptionalResultsRule[_State,_Result]",
            "MultipleResultsRule[_State,_Result]",
            "named_results_rule.NamedResultsRule[_State,_Result]",
        ],
    ) -> "and_.And[_State,_Result, rule.Rule[_State,_Result]]":
        match rhs:
            case (
                no_results_rule.NoResultsRule()
                | single_results_rule.SingleResultsRule()
                | optional_results_rule.OptionalResultsRule()
                | MultipleResultsRule()
            ):
                return multiple_results_and.MultipleResultsAnd[_State, _Result](
                    [self, rhs]
                )
            case named_results_rule.NamedResultsRule():
                return named_results_and.NamedResultsAnd[_State, _Result]([self, rhs])
            case _:
                raise self._error("invalid and rhs {rhs}")


from pysh.core.parser.rules import (
    no_results_rule,
    single_results_rule,
    optional_results_rule,
    named_results_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    multiple_results_and,
    named_results_and,
)
