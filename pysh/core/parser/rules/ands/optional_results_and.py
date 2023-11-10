from dataclasses import dataclass
from typing import Optional, TypeVar, Union
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules.ands import and_
from pysh.core.parser.rules import optional_results_rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class OptionalResultsAnd(
    and_.And[
        _State,
        _Result,
        Union[
            "no_results_rule.NoResultsRule[_State, _Result]",
            optional_results_rule.OptionalResultsRule[_State, _Result],
        ],
    ],
    optional_results_rule.OptionalResultsRule[_State, _Result],
):
    def __post_init__(self):
        if self._num_children_of_type(optional_results_rule.OptionalResultsRule) != 1:
            raise errors.Error(msg=f"invalid OptionalResultsAnd {self}")

    def __call__(
        self, state: _State
    ) -> states.StateAndOptionalResults[_State, _Result]:
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
                        msg=f"too many OptionalResultsAnd results {result} {child_result}",
                    )
                result = child_result
        return states.StateAndOptionalResults[_State, _Result](
            state, results.OptionalResults[_Result](result)
        )


from pysh.core.parser.rules import no_results_rule
