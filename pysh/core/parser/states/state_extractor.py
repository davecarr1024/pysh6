from abc import ABC, abstractmethod
from typing import Generic, TypeVar

_State = TypeVar("_State", contravariant=True)
_StateValue = TypeVar("_StateValue", covariant=True)


class StateExtractor(ABC, Generic[_State, _StateValue]):
    @abstractmethod
    def __call__(self, state: _State) -> _StateValue:
        ...
