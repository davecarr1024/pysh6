from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Union, overload
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ConvertResult = TypeVar("_ConvertResult")


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
        self, rhs: "no_results_rule.NoResultsRule[_State,_Result]"
    ) -> "single_results_and.SingleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultsRule[_State,_Result]"
    ) -> "multiple_results_and.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_results_rule.OptionalResultsRule[_State,_Result]"
    ) -> "multiple_results_and.MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_results_rule.MultipleResultsRule[_State,_Result]"
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
            "SingleResultsRule[_State,_Result]",
            "optional_results_rule.OptionalResultsRule[_State,_Result]",
            "multiple_results_rule.MultipleResultsRule[_State,_Result]",
            "named_results_rule.NamedResultsRule[_State,_Result]",
        ],
    ) -> "and_.And[_State,_Result, rule.Rule[_State,_Result]]":
        match rhs:
            case no_results_rule.NoResultsRule():
                return single_results_and.SingleResultsAnd[_State, _Result]([self, rhs])
            case SingleResultsRule() | optional_results_rule.OptionalResultsRule() | multiple_results_rule.MultipleResultsRule():
                return multiple_results_and.MultipleResultsAnd[_State, _Result](
                    [self, rhs]
                )
            case named_results_rule.NamedResultsRule():
                return named_results_and.NamedResultsAnd[_State, _Result]([self, rhs])
            case _:
                raise self._error("invalid and rhs {rhs}")


from pysh.core.parser.rules import (
    unary_rule,
    no_results_rule,
    optional_results_rule,
    multiple_results_rule,
    named_results_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    single_results_and,
    multiple_results_and,
    named_results_and,
)
