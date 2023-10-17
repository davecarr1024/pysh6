from dataclasses import dataclass, field
from typing import Sequence
from pysh.core import chars
from pysh.core.tokens import error


@dataclass(frozen=True)
class Token:
    rule_name: str
    value: str
    position: chars.Position = field(default_factory=chars.Position)

    @staticmethod
    def load(rule_name: str, value: Sequence[chars.Char] | chars.Stream) -> "Token":
        if isinstance(value, chars.Stream):
            value = list(value)
        if not value:
            raise error.Error(msg=f"loading token with empty value")
        return Token(
            rule_name, "".join(char.value for char in value), value[0].position
        )