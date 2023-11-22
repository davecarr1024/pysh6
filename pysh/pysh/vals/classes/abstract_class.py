from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional
from pysh.pysh.vals import type


@dataclass(frozen=True)
class AbstractClass(type.Type):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def parent(self) -> Optional["AbstractClass"]:
        return None

    @abstractmethod
    def create(self, *args, **kwargs) -> "abstract_object.AbstractObject":
        ...

    def __call__(self, scope: "scope.Scope", args: "args.Args") -> "val.Val":
        obj = self.create()
        self._try(
            lambda: obj["__init__"].val(scope, args),
            "initializing object",
        )
        return obj


from . import abstract_object
from pysh.pysh.vals import args, scope, val
