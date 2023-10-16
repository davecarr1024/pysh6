from dataclasses import dataclass
from typing import Self

from .. import stream
from . import token, unary_error


@dataclass(frozen=True)
class Stream(stream.Stream[token.Token]):
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
