from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class NamedResultsRule(rule.Rule[_State, _Result]):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndNamedResults[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "no_results_rule.NoResultsRule[_State,_Result]"
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_results_rule.SingleResultsRule[_State,_Result]"
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_Result]"
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_Result]"
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "NamedResultsRule[_State,_Result]"
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
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
    ) -> "named_results_and.NamedResultsAnd[_State,_Result]":
        return named_results_and.NamedResultsAnd[_State, _Result]([self, rhs])


from pysh.core.parser.rules import (
    no_results_rule,
    single_results_rule,
    optional_results_rule,
    multiple_results_rule,
)
from pysh.core.parser.rules.ands import (
    named_results_and,
)
