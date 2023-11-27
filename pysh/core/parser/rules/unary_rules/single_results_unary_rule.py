from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import single_results_rule
from pysh.core.parser.rules.unary_rules import unary_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class SingleResultsUnaryRule(
    single_results_rule.SingleResultsRule[_State, _Result],
    unary_rule.UnaryRule[_State, _Result, _Result],
):
    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        return self._call_child(state).single()
