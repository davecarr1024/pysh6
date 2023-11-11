from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer as lexer_lib, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import (
    single_results_rule,
    state_value_setter_rule,
)


_State = TypeVar("_State")


@dataclass(frozen=True)
class Literal(
    state_value_setter_rule.StateValueSetterRule[
        _State,
        tokens.Token,
        lexer_lib.Result,
    ],
    single_results_rule.SingleResultsRule[_State, tokens.Token],
):
    lexer_rule: lexer_lib.Rule

    def __str__(self) -> str:
        return f"Literal({self.lexer_rule})"

    def lexer(self) -> lexer_lib.Lexer:
        return lexer_lib.Lexer([self.lexer_rule])

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
            raise self._parse_error(state, children=[error])
        raise self._parse_error(
            state, msg=f"failed to get expected token {self.lexer_rule}"
        )

    @classmethod
    def load(
        cls,
        lexer_result_setter: states.StateValueSetter[_State, lexer_lib.Result],
        value: str | lexer_lib.Rule,
    ) -> "Literal[_State]":
        if isinstance(value, str):
            value = lexer_lib.Rule.load(value)
        return Literal[_State](lexer_result_setter, value)

    def token_value(self) -> single_results_rule.SingleResultsRule[_State, str]:
        return self.convert(lambda token: token.value)
