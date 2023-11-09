from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states

from pysh.core.parser.rules import single_results_rule, state_value_setter_rule


_State = TypeVar("_State")


@dataclass(frozen=True)
class Literal(
    state_value_setter_rule.StateValueSetterRule[
        _State,
        tokens.Token,
        lexer.Result,
    ],
    single_results_rule.SingleResultsRule[_State, tokens.Token],
):
    lexer_rule: lexer.Rule

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer([self.lexer_rule])

    def __call__(
        self, state: _State
    ) -> states.StateAndSingleResults[_State, tokens.Token]:
        try:
            lexer_result = self._get_state_value(state)
            if lexer_result.head().rule_name == self.lexer_rule.name:
                return states.StateAndSingleResults[_State, tokens.Token](
                    self._set_state_value(state, lexer_result.tail()),
                    results.SingleResults[tokens.Token](lexer_result.head()),
                )
        except errors.Error as error:
            raise self._error(state, children=[error])
        raise self._error(state, msg=f"failed to get expected token {self.lexer_rule}")
