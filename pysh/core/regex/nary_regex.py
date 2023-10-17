from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence, Sized
from pysh.core.regex import regex


@dataclass(frozen=True)
class NaryRegex(regex.Regex, Sized, Iterable[regex.Regex]):
    _children: Sequence[regex.Regex]

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Iterator[regex.Regex]:
        return iter(self._children)
