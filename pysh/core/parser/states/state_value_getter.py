from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


_State = TypeVar("_State")
_Value = TypeVar("_Value")


class StateValueGetter(ABC, Generic[_State, _Value]):
    @abstractmethod
    def get(self, state: _State) -> _Value:
        ...

    @classmethod
    def load(
        cls, get_func: Callable[[_State], _Value]
    ) -> "StateValueGetter[_State,_Value]":
        GetterState = TypeVar("GetterState")
        GetterValue = TypeVar("GetterValue")

        @dataclass(frozen=True)
        class Getter(StateValueGetter[GetterState, GetterValue]):
            get_func: Callable[[GetterState], GetterValue]

            def get(self, state: GetterState) -> GetterValue:
                return self.get_func(state)

        return Getter[_State, _Value](get_func)
