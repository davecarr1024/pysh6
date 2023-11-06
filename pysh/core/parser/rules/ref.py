from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule, scope, single_results_rule


_State = TypeVar("_State", bound=scope.Scope)
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Ref(
    single_results_rule.SingleResultsRule[_State, _Result],
):
    name: str

    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        return state[self.name](state).single()
