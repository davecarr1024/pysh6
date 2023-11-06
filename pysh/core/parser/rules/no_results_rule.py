from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class NoResultsRule(
    Generic[_State, _Result],
    rule.Rule[_State, results.NoResults[_Result], _Result],
):
    @abstractmethod
    def __call__(self, state: _State) -> states.StateAndNoResults[_State, _Result]:
        ...

    def convert(
        self, func: Callable[[], _Result]
    ) -> "single_results_rule.SingleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")

        @dataclass(frozen=True)
        class Converter(
            Generic[AdapterState, AdapterResult],
            single_results_rule.SingleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[
                AdapterState,
                results.SingleResults[AdapterResult],
                AdapterResult,
                results.NoResults[AdapterResult],
            ],
        ):
            func: Callable[[], AdapterResult]

            def __call__(
                self,
                state: AdapterState,
            ) -> states.StateAndSingleResults[AdapterState, AdapterResult]:
                return self._call_child(state).convert(self.func)

        return Converter[_State, _Result](self, func)


from pysh.core.parser.rules import single_results_rule, unary_rule
