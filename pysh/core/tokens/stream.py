from dataclasses import dataclass
from pysh.core import streams
from pysh.core.tokens import token


@dataclass(frozen=True)
class Stream(streams.Stream[token.Token, "Stream"]):
    def __str__(self) -> str:
        if len(self) == 0:
            return "[]"
        else:
            return f"{repr([str(token) for token in list(self)[:10]])}@{self.head().position}"
