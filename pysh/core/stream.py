from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized, TypeVar
from . import errors


_Item = TypeVar('_Item', covariant=True)

@dataclass(frozen=True)
class Stream(Sized, Iterable[_Item]):
    _items: Sequence[_Item] = field(default_factory=list[_Item])

    def __len__(self)->int:
        return len(self._items)
    
    def __iter__(self)->Iterator[_Item]:
        return iter(self._items)
    
    def __bool__(self)->bool:
        return len(self) > 0
    
    def head(self)->_Item:
        if not self:
            raise errors.Error(msg=f'head from empty stream')
        return self._items[0]
    
    def tail(self)->'Stream[_Item]':
        if not self:
            raise errors.Error(msg=f'tail from empty stream')
        return Stream[_Item](self._items[1:])