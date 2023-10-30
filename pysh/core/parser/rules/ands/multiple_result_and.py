from dataclasses import dataclass
from pysh.core.parser import errors, results, states

from pysh.core.parser.rules import multiple_result_rule, rule, scope
from pysh.core.parser.rules.ands import and_


@dataclass(frozen=True)
class MultipleResultAnd(
    multiple_result_rule.MultipleResultRule[results.Result],
    and_.And[
        results.Result,
        rule.Rule[results.Result],
    ],
):
    def __call__(
        self, state: "states.State"
    ) -> "states.StateAndMultipleResult[results.Result]":
        results_ = results.MultipleResult[results.Result]()
        for child in self:
            try:
                child_state_and_result = child(state)
            except errors.Error as child_error:
                raise errors.ParseError(rule=self, state=state, _children=[child_error])
            state = child_state_and_result.state
            results_ |= child_state_and_result.results.multiple()
        return states.StateAndMultipleResult[results.Result](state, results_)
