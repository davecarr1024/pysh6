from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Sequence, Sized, TypeVar
from pysh.core.regex import regex

_Child = TypeVar("_Child", bound=regex.Regex)


@dataclass(frozen=True)
class NaryRegex(
    Generic[_Child],
    regex.Regex,
    Sized,
    Iterable[_Child],
):
    _children: Sequence[_Child]

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self) -> Iterator[_Child]:
        return iter(self._children)
