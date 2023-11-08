from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors
from pysh.core.parser import states
from pysh.core.parser.rules import scope, single_results_rule, state_extractor_rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Ref(
    single_results_rule.SingleResultsRule[_State, _Result],
    state_extractor_rule.StateExtractorRule[
        _State,
        _Result,
        states.StateAndSingleResults[_State, _Result],
        scope.Scope[_State, _Result],
    ],
):
    name: str

    def _call_with_state_value(
        self, state: _State, scope: scope.Scope[_State, _Result]
    ) -> states.StateAndSingleResults[_State, _Result]:
        if self.name not in scope:
            raise self._error(state, msg=f"unknown rule {self.name}")
        try:
            return scope[self.name](state)
        except errors.Error as error:
            raise self._error(state, children=[error])
