from dataclasses import dataclass, field
from typing import Iterable, Iterator, MutableSequence, Optional, Sequence, Sized
from . import errors, stream


@dataclass(frozen=True)
class Position:
    line: int = 0
    column: int = 0

    def __add__(self, char: 'Char')->'Position':
        if char.value == '\n':
            return Position(self.line+1,0)
        else:
            return Position(self.line,self.column+1)
        
@dataclass(frozen=True)
class Char:
    value: str
    position: Position = field(default_factory=Position)

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f'invalid char {self}')
        
@dataclass(frozen=True)
class Stream(stream.Stream[Char]):
    def __str__(self)->str:
        if not self:
            return '[]'
        else:
            return f'[{"".join([char.value for char in self])}]@{self._items[0].position}'
    
    @staticmethod
    def load(value:str, starting_position: Optional[Position] = None)->'Stream':
        chars: MutableSequence[Char] = []
        position: Position = starting_position or Position()
        for c in value:
            char = Char(c,position)
            chars.append(char)
            position += char
        return Stream(chars)