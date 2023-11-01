from dataclasses import dataclass
from pysh.core.parser import errors, results, states

from pysh.core.parser.rules import named_result_rule, rule, scope
from pysh.core.parser.rules.ands import and_


@dataclass(frozen=True)
class NamedResultAnd(
    named_result_rule.NamedResultRule[results.Result],
    and_.And[
        results.Result,
        rule.Rule[results.Result],
    ],
):
    def __call__(
        self,
        state: states.State,
        scope: scope.Scope[results.Result],
    ) -> "states.StateAndNamedResult[results.Result]":
        results_ = results.NamedResult[results.Result]()
        for child in self:
            try:
                child_state_and_result = child(state, scope)
            except errors.Error as child_error:
                raise errors.ParseError(rule=self, state=state, _children=[child_error])
            state = child_state_and_result.state
            results_ |= child_state_and_result.results.named()
        return states.StateAndNamedResult[results.Result](state, results_)
