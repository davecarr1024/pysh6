from abc import abstractmethod
from dataclasses import dataclass
from typing import final
from pysh.pysh import state
from pysh.pysh.vals import args, type, val
from pysh.pysh.vals.builtins import func_


@dataclass(frozen=True)
class AbstractFunc(val.Val):
    @property
    @final
    def type(self) -> type.Type:
        return func_

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def __call__(self, state: state.State, args: args.Args) -> val.Val:
        ...
