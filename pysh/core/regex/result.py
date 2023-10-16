from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized
from .. import chars, errors, tokens


@dataclass(frozen=True)
class Result(Sized, Iterable[chars.Char]):
    _chars: Sequence[chars.Char] = field(default_factory=list[chars.Char])

    def __str__(self) -> str:
        return self.value()

    def __bool__(self) -> bool:
        return len(self) != 0

    def __len__(self) -> int:
        return len(self._chars)

    def __iter__(self) -> Iterator[chars.Char]:
        return iter(self._chars)

    def __add__(self, rhs: "Result") -> "Result":
        return Result(list(self._chars) + list(rhs._chars))

    def position(self) -> chars.Position:
        if not self:
            raise errors.Error(msg=f"position of empty result")
        return self._chars[0].position

    def value(self) -> str:
        return "".join([char.value for char in self._chars])

    def token(self, rule_name: str) -> tokens.Token:
        return tokens.Token(rule_name, self.value(), self.position())

    @staticmethod
    def load(value: str, position: Optional[chars.Position] = None) -> "Result":
        return Result(list(chars.Stream.load(value, position)))
