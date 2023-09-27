from dataclasses import dataclass, field
from typing import Iterable, Iterator, MutableSequence, Optional, Sequence, Sized
from . import errors


@dataclass(frozen=True)
class Position:
    line: int = 0
    column: int = 0

    def __add__(self, char: 'Char')->'Position':
        if char.value == '\n':
            return Position(self.line+1,0)
        else:
            return Position(0,self.column+1)
        
@dataclass(frozen=True)
class Char:
    value: str
    position: Position = field(default_factory=Position)

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f'invalid char {self}')
        
@dataclass(frozen=True)
class Stream(Sized, Iterable[Char]):
    _chars: Sequence[Char] = field(default_factory=list[Char])

    def __bool__(self)->bool:
        return len(self) != 0
    
    def __len__(self)->int:
        return len(self._chars)
    
    def __iter__(self)->Iterator[Char]:
        return iter(self._chars)
    
    def head(self)->Char:
        if not self:
            raise errors.Error(msg='head from empty CharStream')
        return self._chars[0]
    
    def tail(self)->'Stream':
        if not self:
            raise errors.Error(msg='tail from empty CharStream')
        return Stream(self._chars[1:])
    
    @staticmethod
    def load(value:str, starting_position: Optional[Position] = None)->'Stream':
        chars: MutableSequence[Char] = []
        position: Position = starting_position or Position()
        for c in value:
            char = Char(c,position)
            chars.append(char)
            position += char
        return Stream(chars)