from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Sequence, Sized, TypeVar
from pysh.core import errors


_Item = TypeVar("_Item", covariant=True)
_Stream = TypeVar("_Stream", bound="Stream")


@dataclass(frozen=True)
class Stream(
    Generic[_Item, _Stream],
    Sized,
    Iterable[_Item],
    errors.Errorable["Stream"],
):
    _items: Sequence[_Item] = field(default_factory=list[_Item])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[_Item]:
        return iter(self._items)

    def head(self) -> _Item:
        if len(self) == 0:
            raise self._error(msg="empty stream")
        return list(self)[0]

    def tail(self: _Stream) -> _Stream:
        if len(self) == 0:
            raise self._error(msg="empty stream")
        return self.__class__(list(self._items)[1:])
