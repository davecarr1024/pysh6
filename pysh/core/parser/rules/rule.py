from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, Sequence, TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import results, states


_State = TypeVar("_State")
_Results = TypeVar("_Results", bound=results.Results)
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Rule(ABC, Generic[_State, _Results, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State
    ) -> states.StateAndResults[_State, _Results, _Result]:
        ...

    @abstractmethod
    def lexer(self) -> lexer.Lexer:
        ...

    def _error(
        self,
        state: _State,
        *,
        msg: Optional[str] = None,
        children: Sequence[errors.Error] = []
    ) -> "error.Error[_State,_Results,_Result]":
        return error.Error[_State, _Results, _Result](
            rule=self, state=state, msg=msg, _children=children
        )

    def zero_or_more(
        self,
    ) -> "multiple_results_rule.MultipleResultsRule[_State,_Result]":
        AdapterState = TypeVar("AdapterState")
        AdapterResult = TypeVar("AdapterResult")
        AdapterChildResults = TypeVar("AdapterChildResults", bound=results.Results)

        @dataclass(frozen=True)
        class ZeroOrMore(
            Generic[AdapterState, AdapterResult, AdapterChildResults],
            multiple_results_rule.MultipleResultsRule[AdapterState, AdapterResult],
            unary_rule.UnaryRule[
                AdapterState,
                results.MultipleResults[AdapterResult],
                AdapterResult,
                AdapterChildResults,
            ],
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

        return ZeroOrMore[_State, _Result, _Results](self)


from pysh.core.parser.rules import error, multiple_results_rule, unary_rule
