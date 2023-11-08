from dataclasses import dataclass, field
from typing import Generic, TypeVar
from pysh.core.parser.states import (
    abstract_lexer_state,
    lexer_state_value,
    state_extractor,
)

_State = TypeVar("_State", bound="LexerState")


@dataclass(frozen=True)
class LexerState(
    Generic[_State],
    abstract_lexer_state.AbstractLexerState["LexerState"],
):
    lexer_value: lexer_state_value.LexerStateValue = field(
        default_factory=lexer_state_value.LexerStateValue
    )

    def with_lexer_state_value(
        self, value: lexer_state_value.LexerStateValue
    ) -> "LexerState":
        return LexerState(value)

    @classmethod
    def lexer_state_extractor(
        cls,
    ) -> state_extractor.StateExtractor[
        "LexerState", lexer_state_value.LexerStateValue
    ]:
        class Extractor(
            state_extractor.StateExtractor[
                LexerState, lexer_state_value.LexerStateValue
            ]
        ):
            def __call__(self, state: LexerState) -> lexer_state_value.LexerStateValue:
                return state.lexer_value

            def state_with_value(
                self, state: LexerState, value: lexer_state_value.LexerStateValue
            ) -> LexerState:
                return LexerState(value)

        return Extractor()
