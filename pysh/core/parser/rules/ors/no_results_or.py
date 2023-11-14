from dataclasses import dataclass
from typing import Generic, MutableSequence, TypeVar
from pysh.core import errors
from pysh.core.parser import states
from pysh.core.parser.rules import no_results_rule
from pysh.core.parser.rules.ors import or_


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class NoResultsOr(
    Generic[_State, _Result, _RhsResult],
    or_.Or[
        _State,
        _Result | _RhsResult,
        no_results_rule.NoResultsRule[_State, _Result]
        | no_results_rule.NoResultsRule[_State, _RhsResult],
    ],
    no_results_rule.NoResultsRule[_State, _Result | _RhsResult],
):
    def __call__(
        self, state: _State
    ) -> states.StateAndNoResults[_State, _Result | _RhsResult]:
        errors_: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state)
            except errors.Error as error:
                errors_.append(error)
        raise self._parse_error(state, children=errors_)
