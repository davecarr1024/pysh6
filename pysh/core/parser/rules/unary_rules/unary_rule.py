from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar
from pysh.core import lexer
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_ChildResult = TypeVar("_ChildResult", covariant=True)


@dataclass(frozen=True)
class UnaryRule(
    Generic[_State, _Result, _ChildResult],
    rule.Rule[_State, _Result],
):
    child: rule.Rule[_State, _ChildResult]
    _lexer: Optional[lexer.Lexer] = field(default=None, kw_only=True)

    def __str__(self) -> str:
        return (
            str(self.child)
            if self._lexer is None
            else f"{self.child}.with_lexer({self._lexer})"
        )

    def _call_child(
        self, state: _State
    ) -> states.StateAndResults[_State, _ChildResult]:
        return self._try(lambda: self.child(state))

    def lexer(self) -> lexer.Lexer:
        return (
            self.child.lexer() | self._lexer
            if self._lexer is not None
            else self.child.lexer()
        )
