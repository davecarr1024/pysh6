from dataclasses import dataclass
from typing import MutableSequence, Optional
from pysh.core import streams


@dataclass(frozen=True)
class Stream(streams.Stream["char.Char", "Stream"]):
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


from pysh.core.chars import char, position
