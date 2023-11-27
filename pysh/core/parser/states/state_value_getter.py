from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from pysh.core.parser.states import state


_State = TypeVar("_State", bound=state.State)
_Value = TypeVar("_Value", covariant=True)


class StateValueGetter(ABC, Generic[_State, _Value]):
    @abstractmethod
    def get(self, state: _State) -> _Value:
        ...

    @classmethod
    def load(
        cls, get_func: Callable[[_State], _Value]
    ) -> "StateValueGetter[_State,_Value]":
        return _Getter[_State, _Value](get_func)


@dataclass(frozen=True)
class _Getter(StateValueGetter[_State, _Value]):
    get_func: Callable[[_State], _Value]

    def get(self, state: _State) -> _Value:
        return self.get_func(state)
