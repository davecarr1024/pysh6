from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Self, Sequence, Sized, TypeVar
from . import error


_Item = TypeVar("_Item", covariant=True)


@dataclass(frozen=True)
class Stream(Generic[_Item], Sized, Iterable[_Item]):
    _items: Sequence[_Item] = field(default_factory=list[_Item])

    def __str__(self) -> str:
        return f'[{", ".join(str(item) for item in self)}]'

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[_Item]:
        return iter(self._items)

    def __bool__(self) -> bool:
        return len(self) > 0

    def head(self) -> _Item:
        if not self:
            raise error.Error(msg=f"head from empty stream")
        return self._items[0]

    def tail(self) -> Self:
        if not self:
            raise error.Error(msg=f"tail from empty stream")
        return self.__class__(self._items[1:])
