from dataclasses import dataclass, field
from typing import Sequence
from pysh.core import chars, errors


@dataclass(frozen=True)
class Token(errors.Errorable["Token"]):
    rule_name: str
    value: str
    position: chars.Position = field(default_factory=chars.Position)

    def __str__(self) -> str:
        if self.rule_name == self.value:
            return self.rule_name
        return f"{self.rule_name}({self.value})"

    @classmethod
    def load(
        cls, rule_name: str, value: Sequence[chars.Char] | chars.Stream
    ) -> "Token":
        if isinstance(value, chars.Stream):
            value = list(value)
        if not value:
            raise cls._cls_error(msg=f"loading token with empty value")
        return Token(
            rule_name, "".join(char.value for char in value), value[0].position
        )
