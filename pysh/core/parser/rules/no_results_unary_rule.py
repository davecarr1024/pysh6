from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import no_results_rule, unary_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_ChildResult = TypeVar("_ChildResult", covariant=True)


@dataclass(frozen=True)
class NoResultsUnaryRule(
    Generic[_State, _Result, _ChildResult],
    no_results_rule.NoResultsRule[_State, _Result],
    unary_rule.UnaryRule[_State, _Result, _ChildResult],
):
    def __call__(self, state: _State) -> states.StateAndNoResults[_State, _Result]:
        return states.StateAndNoResults[_State, _Result](self._call_child(state).state)
