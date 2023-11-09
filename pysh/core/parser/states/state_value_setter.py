from abc import ABC, abstractmethod
from typing import Generic, TypeVar


_State = TypeVar("_State")
_Value = TypeVar("_Value")


class StateValueSetter(ABC, Generic[_State, _Value]):
    @abstractmethod
    def get(self, state: _State) -> _Value:
        ...

    @abstractmethod
    def set(self, state: _State, value: _Value) -> _State:
        ...
