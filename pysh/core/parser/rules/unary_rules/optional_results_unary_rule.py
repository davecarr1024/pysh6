from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import optional_results_rule
from pysh.core.parser.rules.unary_rules import unary_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class OptionalResultsUnaryRule(
    optional_results_rule.OptionalResultsRule[_State, _Result],
    unary_rule.UnaryRule[_State, _Result, _Result],
):
    def __call__(
        self, state: _State
    ) -> states.StateAndOptionalResults[_State, _Result]:
        return self._call_child(state).optional()
