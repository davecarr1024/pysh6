from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors
from pysh.core.parser import states
from pysh.core.parser.rules import no_results_rule
from pysh.core.parser.rules.ands import and_


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class NoResultsAnd(
    and_.And[_State, _Result, no_results_rule.NoResultsRule[_State, _Result]],
    no_results_rule.NoResultsRule[_State, _Result],
):
    def __call__(self, state: _State) -> states.StateAndNoResults[_State, _Result]:
        for child in self:
            try:
                state = child(state).state
            except errors.Error as error:
                raise self._state_error(state, children=[error])
        return states.StateAndNoResults[_State, _Result](state)
