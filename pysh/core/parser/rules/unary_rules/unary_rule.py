from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar
from pysh.core import errors, lexer
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import child_rule, rule, scope as scope_lib


@dataclass(frozen=True)
class UnaryRule(
    Generic[results.Result, child_rule.ChildRule],
    rule.Rule[results.Result],
):
    child: child_rule.ChildRule
    scope: Optional[scope_lib.Scope[results.Result]] = field(default=None, kw_only=True)

    def __str__(self) -> str:
        return str(self.child)

    def _scope(
        self, scope: scope_lib.Scope[results.Result]
    ) -> scope_lib.Scope[results.Result]:
        return (self.scope or scope_lib.Scope[results.Result]()) | scope

    def _call(
        self, state: states.State, scope: scope_lib.Scope[results.Result]
    ) -> states.StateAndResult[results.Result]:
        try:
            return self.child(state, self._scope(scope))
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
