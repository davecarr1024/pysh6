from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Union
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules.ands import and_
from pysh.core.parser.rules import optional_results_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class OptionalResultsAnd(
    Generic[_State, _Result, _RhsResult],
    and_.And[
        _State,
        _Result | _RhsResult,
        Union[
            "no_results_rule.NoResultsRule[_State, _Result]",
            optional_results_rule.OptionalResultsRule[_State, _Result],
            "no_results_rule.NoResultsRule[_State, _RhsResult]",
            optional_results_rule.OptionalResultsRule[_State, _RhsResult],
        ],
    ],
    optional_results_rule.OptionalResultsRule[_State, _Result | _RhsResult],
):
    def __post_init__(self):
        if self._num_children_of_type(optional_results_rule.OptionalResultsRule) != 1:
            raise errors.Error(msg=f"invalid OptionalResultsAnd {self}")

    def __call__(
        self, state: _State
    ) -> states.StateAndOptionalResults[_State, _Result | _RhsResult]:
        result: Optional[_Result | _RhsResult] = None
        for child in self:
            try:
                child_state_and_result = child(state)
            except errors.Error as error:
                raise self._parse_error(state, children=[error])
            state = child_state_and_result.state
            child_result = child_state_and_result.results.optional().value
            if child_result is not None:
                if result is not None:
                    raise self._parse_error(
                        state,
                        msg=f"too many OptionalResultsAnd results {result} {child_result}",
                    )
                result = child_result
        return states.StateAndOptionalResults[_State, _Result | _RhsResult](
            state, results.OptionalResults[_Result | _RhsResult](result)
        )


from pysh.core.parser.rules import no_results_rule
