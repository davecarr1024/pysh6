from dataclasses import dataclass, field
from typing import Self
from pysh.core import lexer, tokens


@dataclass(frozen=True)
class State:
    lexer_result: lexer.Result = field(default_factory=lexer.Result)

    def __str__(self) -> str:
        return str(self.lexer_result)

    def with_lexer_result(self, lexer_result: lexer.Result) -> Self:
        return self.__class__(lexer_result)

    def head(self) -> tokens.Token:
        return self.lexer_result.head()

    def tail(self) -> Self:
        return self.with_lexer_result(self.lexer_result.tail())
