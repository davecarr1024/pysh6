from dataclasses import dataclass
from typing import Generic, MutableSequence, Optional, TypeVar, Union
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import single_results_rule
from pysh.core.parser.rules.ors import or_


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class SingleResultsOr(
    Generic[_State, _Result, _RhsResult],
    or_.Or[
        _State,
        _Result | _RhsResult,
        Union[
            single_results_rule.SingleResultsRule[_State, _Result],
            single_results_rule.SingleResultsRule[_State, _RhsResult],
        ],
    ],
    single_results_rule.SingleResultsRule[_State, _Result | _RhsResult],
):
    def __call__(
        self, state: _State
    ) -> states.StateAndSingleResults[_State, _Result | _RhsResult]:
        errors_: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state)
            except errors.Error as error:
                errors_.append(error)
        raise self._state_error(state, children=errors_)
