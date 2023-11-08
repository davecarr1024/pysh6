from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import lexer_rule, single_results_rule
from pysh.core.parser.states import lexer_state_value


_State = TypeVar("_State")


@dataclass(frozen=True)
class Literal(
    lexer_rule.LexerRule[
        _State,
        tokens.Token,
        states.StateAndSingleResults[_State, tokens.Token],
    ],
    single_results_rule.SingleResultsRule[_State, tokens.Token],
):
    lexer_rule: lexer.Rule

    def lexer(self) -> lexer.Lexer:
        return lexer.Lexer([self.lexer_rule])

    def _call_with_state_value(
        self,
        state: _State,
        state_value: lexer_state_value.LexerStateValue,
    ) -> states.StateAndSingleResults[_State, tokens.Token]:
        try:
            if state_value.head().rule_name == self.lexer_rule.name:
                return states.StateAndSingleResults[_State, tokens.Token](
                    self._state_with_value(state, state_value.tail()),
                    results.SingleResults[tokens.Token](state_value.head()),
                )
        except errors.Error as error:
            raise self._error(state, children=[error])
        raise self._error(state, msg=f"failed to find literal {self.lexer_rule}")
