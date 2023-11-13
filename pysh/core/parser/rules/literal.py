from dataclasses import dataclass
from typing import TypeVar
from pysh.core import errors, lexer as lexer_lib, tokens
from pysh.core.parser import results, states
from pysh.core.parser.rules import single_results_rule


_State = TypeVar("_State", bound=states.State)


@dataclass(frozen=True)
class Literal(
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
            if state.head().rule_name == self.lexer_rule.name:
                return states.StateAndSingleResults[_State, tokens.Token](
                    state.tail(),
                    results.SingleResults[tokens.Token](state.head()),
                )
        except errors.Error as error:
            raise self._parse_error(state, children=[error])
        raise self._parse_error(
            state, msg=f"failed to get expected token {self.lexer_rule}"
        )

    @classmethod
    def load(
        cls,
        value: str | lexer_lib.Rule,
    ) -> "Literal[_State]":
        if isinstance(value, str):
            value = lexer_lib.Rule.load(value)
        return Literal[_State](value)

    def token_value(self) -> single_results_rule.SingleResultsRule[_State, str]:
        return self.convert(lambda token: token.value)
