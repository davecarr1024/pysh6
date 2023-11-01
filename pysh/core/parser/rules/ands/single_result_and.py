from dataclasses import dataclass
from typing import Optional
from pysh.core.parser import errors, results, states
from pysh.core.parser.rules import no_result_rule, scope, single_result_rule
from pysh.core.parser.rules.ands import and_


@dataclass(frozen=True)
class SingleResultAnd(
    single_result_rule.SingleResultRule[results.Result],
    and_.And[
        results.Result,
        no_result_rule.NoResultRule[results.Result]
        | single_result_rule.SingleResultRule[results.Result],
    ],
):
    def __post_init__(self):
        self._assert_num_children_of_type(single_result_rule.SingleResultRule, 1)

    def __call__(
        self,
        state: states.State,
        scope: scope.Scope[results.Result],
    ) -> "states.StateAndSingleResult[results.Result]":
        result: Optional[results.Result] = None
        for child in self:
            try:
                child_state_and_result = child(state, scope)
            except errors.Error as child_error:
                raise errors.ParseError(rule=self, state=state, _children=[child_error])
            state = child_state_and_result.state
            child_result = child_state_and_result.optional().results.result
            if child_result is not None:
                if result is not None:
                    raise errors.ParseError(
                        rule=self,
                        state=state,
                        msg=f"duplicate results for SingleResultAnd {result} {child_result}",
                    )
                result = child_result
        if result is None:
            raise errors.ParseError(
                rule=self, state=state, msg="no result for SingleResultAnd"
            )
        return states.StateAndSingleResult[results.Result](
            state, results.SingleResult[results.Result](result)
        )
