from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import multiple_results_rule
from pysh.core.parser.rules.unary_rules import unary_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class MultipleResultsUnaryRule(
    multiple_results_rule.MultipleResultsRule[_State, _Result],
    unary_rule.UnaryRule[_State, _Result, _Result],
):
    def __call__(
        self, state: _State
    ) -> states.StateAndMultipleResults[_State, _Result]:
        return self._call_child(state).multiple()
