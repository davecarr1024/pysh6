from dataclasses import dataclass
from typing import Optional
from pysh.core.parser import errors, results, states
from pysh.core.parser.rules import no_result_rule, scope, optional_result_rule
from pysh.core.parser.rules.ands import and_


@dataclass(frozen=True)
class OptionalResultAnd(
    optional_result_rule.OptionalResultRule[results.Result],
    and_.And[
        results.Result,
        no_result_rule.NoResultRule[results.Result]
        | optional_result_rule.OptionalResultRule[results.Result],
    ],
):
    def __post_init__(self):
        self._assert_num_children_of_type(optional_result_rule.OptionalResultRule, 1)

    def __call__(
        self,
        state: states.State,
        scope: scope.Scope[results.Result],
    ) -> "states.StateAndOptionalResult[results.Result]":
        result: Optional[results.Result] = None
        for child in self:
            try:
                child_state_and_result = child(state, scope)
            except errors.Error as error:
                raise errors.ParseError(rule=self, state=state, _children=[error])
            state = child_state_and_result.state
            child_result = child_state_and_result.optional().results.result
            if child_result is not None:
                if result is not None:
                    raise errors.ParseError(
                        rule=self,
                        state=state,
                        msg=f"duplicate results for OptionalResultAnd {result} {child_result}",
                    )
                result = child_result
        return states.StateAndOptionalResult[results.Result](
            state, results.OptionalResult[results.Result](result)
        )
