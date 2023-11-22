from abc import abstractmethod
from dataclasses import dataclass
from pysh.pysh import state
from pysh.pysh.vals import args, scope, val


@dataclass(frozen=True)
class AbstractObject(val.Val):
    @property
    @abstractmethod
    def type(self) -> "abstract_class.AbstractClass":
        ...

    def __call__(self, state: state.State, args: args.Args) -> val.Val:
        return self._try(
            lambda: self["__call__"].val(state, args),
            "failed to call object's __call__",
        )


from . import abstract_class
