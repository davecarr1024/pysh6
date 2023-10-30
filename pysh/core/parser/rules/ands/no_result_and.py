from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import no_result_rule, scope

from pysh.core.parser.rules.ands import and_


@dataclass(frozen=True)
class NoResultAnd(
    no_result_rule.NoResultRule[results.Result],
    and_.And[results.Result, no_result_rule.NoResultRule[results.Result]],
):
    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndNoResult[results.Result]:
        for child in self:
            child_state_and_result = child(state, scope)
            state = child_state_and_result.state
        return states.StateAndNoResult[results.Result](state, results.NoResult())
