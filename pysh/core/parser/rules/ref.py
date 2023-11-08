from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import states
from pysh.core.parser.rules import (
    scope,
    scope_rule,
    single_results_rule,
)


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class Ref(
    scope_rule.ScopeRule[
        _State,
        _Result,
        states.StateAndSingleResults[_State, _Result],
    ],
    single_results_rule.SingleResultsRule[_State, _Result],
):
    name: str

    def _call_with_state_value(
        self, state: _State, scope: scope.Scope[_State, _Result]
    ) -> states.StateAndSingleResults[_State, _Result]:
        if self.name not in scope:
            raise self._error(state, msg=f"unknown rule {self.name}")
        try:
            return scope[self.name](state)
        except errors.Error as error:
            raise self._error(state, children=[error])

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer()
