from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Results = TypeVar("_Results", bound=results.Results)
_Result = TypeVar("_Result")
_ChildResults = TypeVar("_ChildResults", bound=results.Results)


@dataclass(frozen=True)
class UnaryRule(
    Generic[_State, _Results, _Result, _ChildResults],
    rule.Rule[_State, _Results, _Result],
):
    child: rule.Rule[_State, _ChildResults, _Result]

    def _call_child(
        self, state: _State
    ) -> states.StateAndResults[_State, _ChildResults, _Result]:
        try:
            return self.child(state)
        except errors.Error as error:
            raise self._error(state, children=[error])

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
