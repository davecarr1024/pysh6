from dataclasses import dataclass
from typing import Generic, MutableSequence, TypeVar, Union
from pysh.core import errors
from pysh.core.parser import states
from pysh.core.parser.rules import (
    named_results_rule,
    rule,
)
from pysh.core.parser.rules.ors import or_


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class NamedResultsOr(
    Generic[_State, _Result, _RhsResult],
    or_.Or[
        _State,
        _Result | _RhsResult,
        Union[
            rule.Rule[_State, _Result],
            rule.Rule[_State, _RhsResult],
        ],
    ],
    named_results_rule.NamedResultsRule[_State, _Result | _RhsResult],
):
    def __call__(
        self, state: _State
    ) -> states.StateAndNamedResults[_State, _Result | _RhsResult]:
        errors_: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state).named()
            except errors.Error as error:
                errors_.append(error)
        raise self._state_error(state, children=errors_)
