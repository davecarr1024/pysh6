from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import states
from pysh.core.parser.rules import scope, single_results_rule, state_value_getter_rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class Ref(
    state_value_getter_rule.StateValueGetterRule[
        _State,
        _Result,
        scope.Scope[_State, _Result],
    ],
    single_results_rule.SingleResultsRule[_State, _Result],
):
    name: str

    def __str__(self) -> str:
        return f"Ref({self.name})"

    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        scope = self._get_state_value(state)
        if self.name not in scope:
            raise self._parse_error(state, msg=f"unknown rule {self.name}")
        try:
            return scope[self.name](state)
        except errors.Error as error:
            raise self._parse_error(state, children=[error])
