from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import named_results_rule, rule
from pysh.core.parser.rules.ands import and_


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class NamedResultsAnd(
    and_.And[
        _State,
        _Result,
        rule.Rule[_State, _Result],
    ],
    named_results_rule.NamedResultsRule[_State, _Result],
):
    def __call__(self, state: _State) -> states.StateAndNamedResults[_State, _Result]:
        results_ = results.NamedResults[_Result]()
        for child in self:
            try:
                child_state_and_result = child(state)
                state = child_state_and_result.state
                results_ |= child_state_and_result.results.named()
            except errors.Error as error:
                raise self._state_error(state, children=[error])
        return states.StateAndNamedResults[_State, _Result](state, results_)
