from dataclasses import dataclass
from typing import MutableSequence, Optional, Self
from pysh.core import stream
from pysh.core.chars import unary_error


@dataclass(frozen=True)
class Stream(stream.Stream["char.Char"]):
    def __str__(self) -> str:
        if not self:
            return "[]"
        else:
            return (
                f'[{"".join([char.value for char in self])}]@{self._items[0].position}'
            )

    @staticmethod
    def load(
        value: str, starting_position: Optional["position.Position"] = None
    ) -> "Stream":
        chars: MutableSequence[char.Char] = []
        position_: position.Position = starting_position or position.Position()
        for c in value:
            char_ = char.Char(c, position_)
            chars.append(char_)
            position_ += char_
        return Stream(chars)

    def head(self) -> "char.Char":
        try:
            return super().head()
        except stream.Error as error_:
            raise unary_error.UnaryError(child=error_)

    def tail(self) -> Self:
        try:
            return super().tail()
        except stream.Error as error_:
            raise unary_error.UnaryError(child=error_)


from pysh.core.chars import char, position
