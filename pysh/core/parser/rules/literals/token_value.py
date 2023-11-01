from dataclasses import dataclass
from pysh.core import errors, lexer
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import scope, single_result_rule


@dataclass(frozen=True)
class TokenValue(single_result_rule.SingleResultRule[str]):
    lexer_rule: lexer.Rule

    def __call__(
        self, state: "states.State", scope: "scope.Scope[str]"
    ) -> "states.StateAndSingleResult[str]":
        try:
            if state.head().rule_name == self.lexer_rule.name:
                return states.StateAndSingleResult[str](
                    state.tail(), results.SingleResult[str](state.head().value)
                )
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])
        raise parse_error.ParseError(
            rule=self, state=state, msg=f"expected rule_name {self.lexer_rule.name}"
        )

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer([self.lexer_rule])
