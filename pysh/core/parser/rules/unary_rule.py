from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(frozen=True)
class UnaryRule(
    rule.Rule[_State, _Result],
):
    child: rule.Rule[_State, _Result]

    def _call_child(self, state: _State) -> states.StateAndResults[_State, _Result]:
        try:
            return self.child(state)
        except errors.Error as error:
            raise self._error(state, children=[error])

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
