from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import multiple_results_rule
from pysh.core.parser.rules.unary_rules import unary_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class ZeroOrMore(
    multiple_results_rule.MultipleResultsRule[_State, _Result],
    unary_rule.UnaryRule[_State, _Result, _Result],
):
    def __str__(self) -> str:
        return f"{super().__str__()}*"

    def __call__(
        self, state: _State
    ) -> states.StateAndMultipleResults[_State, _Result]:
        results_ = results.MultipleResults[_Result]()
        while True:
            try:
                state_and_results = self._call_child(state)
                state = state_and_results.state
                results_ |= state_and_results.results.multiple()
            except errors.Error:
                return states.StateAndMultipleResults[_State, _Result](state, results_)
