from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


_State = TypeVar("_State")
_Value = TypeVar("_Value")


class StateValueSetter(ABC, Generic[_State, _Value]):
    @abstractmethod
    def get(self, state: _State) -> _Value:
        ...

    @abstractmethod
    def set(self, state: _State, value: _Value) -> _State:
        ...

    @classmethod
    def load(
        cls,
        get_func: Callable[[_State], _Value],
        set_func: Callable[[_State, _Value], _State],
    ) -> "StateValueSetter[_State,_Value]":
        SetterState = TypeVar("SetterState")
        SetterValue = TypeVar("SetterValue")

        @dataclass(frozen=True)
        class Setter(StateValueSetter[SetterState, SetterValue]):
            get_func: Callable[[SetterState], SetterValue]
            set_func: Callable[[SetterState, SetterValue], SetterState]

            def get(self, state: SetterState) -> SetterValue:
                return self.get_func(state)

            def set(self, state: SetterState, value: SetterValue) -> SetterState:
                return self.set_func(state, value)

        return Setter[_State, _Value](get_func, set_func)
