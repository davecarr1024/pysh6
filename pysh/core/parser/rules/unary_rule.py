from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_ChildResult = TypeVar("_ChildResult")


@dataclass(frozen=True)
class UnaryRule(
    Generic[_State, _Result, _ChildResult],
    rule.Rule[_State, _Result],
):
    child: rule.Rule[_State, _ChildResult]

    def _call_child(
        self, state: _State
    ) -> states.StateAndResults[_State, _ChildResult]:
        try:
            return self.child(state)
        except errors.Error as error:
            raise self._state_error(state, children=[error])

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
