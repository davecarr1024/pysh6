from dataclasses import dataclass, field
from typing import Generic, Optional

from pysh.core import errors, lexer
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import child_rule, rule, scope


@dataclass(frozen=True)
class UnaryRule(
    Generic[results.Result, child_rule.ChildRule],
    rule.Rule[results.Result],
):
    child: child_rule.ChildRule

    def __str__(self) -> str:
        return str(self.child)

    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndResult[results.Result]:
        try:
            return self.child(state, scope)
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])

    def lexer(self) -> lexer.Lexer:
        return self.child.lexer()
