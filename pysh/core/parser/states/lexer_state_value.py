from dataclasses import dataclass, field
from pysh.core import tokens as tokens_lib


@dataclass(frozen=True)
class LexerStateValue:
    tokens: tokens_lib.Stream = field(default_factory=tokens_lib.Stream)

    def head(self) -> tokens_lib.Token:
        return self.tokens.head()

    def tail(self) -> "LexerStateValue":
        return LexerStateValue(self.tokens.tail())
