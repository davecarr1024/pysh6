from dataclasses import dataclass, field
from typing import Generic
from pysh.core import errors, tokens as tokens_lib
from pysh.core.parser import results
from pysh.core.parser.errors import error


@dataclass(frozen=True)
class State(Generic[results.Result]):
    tokens: tokens_lib.Stream = field(default_factory=tokens_lib.Stream)
    scope: "scope_lib.Scope[results.Result]" = field(
        default_factory=lambda: scope_lib.Scope[results.Result]()
    )

    def tail(self) -> "State":
        try:
            return State(self.tokens.tail())
        except errors.Error as e:
            raise error.Error(msg=f"failed to get state tail: {e}")

    def head(self) -> tokens_lib.Token:
        try:
            return self.tokens.head()
        except errors.Error as e:
            raise error.Error(msg=f"failed to get state head: {e}")


from pysh.core.parser.rules import scope as scope_lib
