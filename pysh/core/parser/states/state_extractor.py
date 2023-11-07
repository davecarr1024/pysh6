from abc import ABC, abstractmethod
from typing import Generic, TypeVar


_State = TypeVar("_State")
_StateValue = TypeVar("_StateValue")


class StateExtractor(ABC, Generic[_State, _StateValue]):
    @abstractmethod
    def state_value(self, state: _State) -> _StateValue:
        ...
