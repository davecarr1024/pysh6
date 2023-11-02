from dataclasses import dataclass
from pysh.core import errors, lexer
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error

from pysh.core.parser.rules import scope, single_result_rule


@dataclass(frozen=True)
class Reference(single_result_rule.SingleResultRule[results.Result]):
    rule_name: str

    def __str__(self) -> str:
        return self.rule_name

    def __call__(
        self,
        state: states.State,
        scope: scope.Scope[results.Result],
    ) -> "states.StateAndSingleResult[results.Result]":
        if self.rule_name not in scope:
            raise parse_error.ParseError(
                rule=self, state=state, msg=f"unknown rule reference {self.rule_name}"
            )
        try:
            return scope[self.rule_name](state, scope)
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer()
