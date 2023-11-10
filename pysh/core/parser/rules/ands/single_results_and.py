from dataclasses import dataclass
from typing import Optional, TypeVar, Union
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import single_results_rule
from pysh.core.parser.rules.ands import and_


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class SingleResultsAnd(
    and_.And[
        _State,
        _Result,
        Union[
            "no_results_rule.NoResultsRule[_State, _Result]",
            single_results_rule.SingleResultsRule[_State, _Result],
        ],
    ],
    single_results_rule.SingleResultsRule[_State, _Result],
):
    def __post_init__(self):
        if self._num_children_of_type(single_results_rule.SingleResultsRule) != 1:
            raise errors.Error(msg=f"invalid SingleResultsAnd {self}")

    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        result: Optional[_Result] = None
        for child in self:
            try:
                child_state_and_result = child(state)
            except errors.Error as error:
                raise self._state_error(state, children=[error])
            state = child_state_and_result.state
            child_result = child_state_and_result.results.optional().value
            if child_result is not None:
                if result is not None:
                    raise self._state_error(
                        state,
                        msg=f"too many SingleResultsAnd results {result} {child_result}",
                    )
                result = child_result
        if result is None:
            raise self._state_error(state, msg="no SingleResultsAnd result")
        return states.StateAndSingleResults[_State, _Result](
            state, results.SingleResults[_Result](result)
        )


from pysh.core.parser.rules import no_results_rule
