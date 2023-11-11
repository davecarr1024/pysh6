from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import multiple_results_rule, rule
from pysh.core.parser.rules.ands import and_


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class MultipleResultsAnd(
    Generic[_State, _Result, _RhsResult],
    and_.And[
        _State,
        _Result | _RhsResult,
        rule.Rule[_State, _Result] | rule.Rule[_State, _RhsResult],
    ],
    multiple_results_rule.MultipleResultsRule[_State, _Result | _RhsResult],
):
    def __call__(
        self, state: _State
    ) -> states.StateAndMultipleResults[_State, _Result | _RhsResult]:
        results_ = results.MultipleResults[_Result | _RhsResult]()
        for child in self:
            try:
                child_state_and_result = child(state)
                state = child_state_and_result.state
                results_ |= child_state_and_result.results.multiple()
            except errors.Error as error:
                raise self._parse_error(state, children=[error])
        return states.StateAndMultipleResults[_State, _Result | _RhsResult](
            state, results_
        )
