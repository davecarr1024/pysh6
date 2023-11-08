from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar
from pysh.core import lexer
from pysh.core.parser.states import lexer_state_value, state_extractor


_State = TypeVar("_State", bound="AbstractLexerState")


class AbstractLexerState(
    ABC,
    Generic[_State],
):
    @abstractmethod
    def with_lexer_state_value(self, value: lexer_state_value.LexerStateValue) -> Self:
        ...

    @classmethod
    @abstractmethod
    def lexer_state_extractor(
        cls,
    ) -> state_extractor.StateExtractor[_State, lexer_state_value.LexerStateValue]:
        ...

    @classmethod
    def literal(cls, lexer_rule: lexer.Rule) -> "rules.Literal[_State]":
        return rules.Literal[_State](cls.lexer_state_extractor(), lexer_rule)


from pysh.core.parser import rules
