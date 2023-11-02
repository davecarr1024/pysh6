from dataclasses import dataclass
from typing import Self

from pysh.core import stream
from pysh.core.tokens import token, unary_error


@dataclass(frozen=True)
class Stream(stream.Stream[token.Token]):
    def __str__(self) -> str:
        if len(self) == 0:
            return "[]"
        else:
            return f"{repr([token.value for token in list(self)[:10]])}@{self.head().position}"

    def head(self) -> "token.Token":
        try:
            return super().head()
        except stream.Error as error_:
            raise unary_error.UnaryError(child=error_)

    def tail(self) -> Self:
        try:
            return super().tail()
        except stream.Error as error_:
            raise unary_error.UnaryError(child=error_)
