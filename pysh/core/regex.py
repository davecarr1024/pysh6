from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Iterator, MutableSequence, Sequence, Sized
from . import chars, errors, tokens

@dataclass(frozen=True, kw_only=True)
class Error(errors.NaryError):
    state: chars.Stream
    regex: 'Regex'

@dataclass(frozen=True)
class Result(Sized, Iterable[chars.Char]):
    _chars: Sequence[chars.Char] = field(default_factory=list[chars.Char])

    def __bool__(self)->bool:
        return len(self) != 0
    
    def __len__(self)->int:
        return len(self._chars)
    
    def __iter__(self)->Iterator[chars.Char]:
        return iter(self._chars)
    
    def __add__(self, rhs: 'Result')->'Result':
        return Result(list(self._chars)+list(rhs._chars))
    
    def position(self)->chars.Position:
        if not self:
            raise errors.Error(msg=f'position of empty result')
        return self._chars[0].position
        
    def value(self)->str:
        return ''.join([char.value for char in self._chars])
    
    def token(self, rule_name: str)->tokens.Token:
        return tokens.Token(rule_name, self.value(), self.position())

StateAndResult = tuple[chars.Stream, Result]

    
class Regex(ABC):
    @abstractmethod
    def __call__(self, state: chars.Stream)->StateAndResult:
        ...

@dataclass(frozen=True)
class Any(Regex):
    def __str__(self)->str:
        return '.'
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        return state.tail(), Result([state.head()])

@dataclass(frozen=True)
class Literal(Regex):
    value: str

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f'invalid literal {self}')

    def __str__(self)->str:
        return self.value
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        if state.head().value != self.value:
            raise Error(regex=self,state=state,msg=f'expected literal {self.value} got {state.head()}')
        return state.tail(), Result([state.head()])

@dataclass(frozen=True)
class Range(Regex):
    start: str
    end: str

    def __post_init__(self):
        if len(self.start) != 1 or len(self.end) != 1:
            raise errors.Error(msg=f'invalid range {self}')
        
    def __str__(self):
        return f'[{self.start}-{self.end}]'
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        if self.start > state.head().value or self.end < state.head().value:
            raise Error(regex=self,state=state)
        return state.tail(), Result([state.head()])

@dataclass(frozen=True)
class _NaryRegex(Regex, Sized, Iterable[Regex]):
    _children: Sequence[Regex]

    def __len__(self)->int:
        return len(self._children)
    
    def __iter__(self)->Iterator[Regex]:
        return iter(self._children)

@dataclass(frozen=True)
class And(_NaryRegex):
    def __str__(self)->str:
        return f"({''.join([str(child) for child in self])})"
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        result = Result()
        for child in self:
            try:
                state, child_result = child(state)
            except errors.Error as error:
                raise Error(regex=self,state=state,children=[error])
            result += child_result
        return state, result

@dataclass(frozen=True)
class Or(_NaryRegex):
    def __str__(self)->str:
        return f"({'|'.join([str(child) for child in self])})"
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        child_errors: MutableSequence[errors.Error] = []
        for child in self:
            try:
                return child(state)
            except errors.Error as error:
                child_errors.append(error)
        raise Error(regex=self,state=state,children=child_errors)

@dataclass(frozen=True)
class _UnaryRegex(Regex):
    child: Regex

@dataclass(frozen=True)
class ZeroOrOne(_UnaryRegex):
    def __str__(self)->str:
        return f'{self.child}?'
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        try:
            return self.child(state)
        except errors.Error:
            return state.tail(), Result()

@dataclass(frozen=True)
class ZeroOrMore(_UnaryRegex):
    def __str__(self)->str:
        return f'{self.child}*'
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        result = Result()
        while True:
            try:
                state, child_result = self.child(state)
                result += child_result
            except errors.Error:
                return state, result

@dataclass(frozen=True)
class OneOrMore(_UnaryRegex):
    def __str__(self)->str:
        return f'{self.child}+'
    
    def __call__(self, state: chars.Stream)->StateAndResult:
        try:
            state, result = self.child(state)
        except errors.Error as error:
            raise Error(regex=self,state=state,children=[error])
        while True:
            try:
                state, child_result = self.child(state)
                result += child_result
            except errors.Error:
                return state, result

