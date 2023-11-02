from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh.core.errors import error


@dataclass(kw_only=True, repr=False)
class NaryError(
    error.Error,
    Sized,
    Iterable[error.Error],
):
    _children: Sequence[error.Error] = field(default_factory=list[error.Error])

    def __iter__(self) -> Iterator[error.Error]:
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)

    def _repr(self, indent: int) -> str:
        s: str = super()._repr(indent)
        for child in self._children:
            s += child._repr(indent + 1)
        return s
