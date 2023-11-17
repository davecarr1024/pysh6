from abc import abstractmethod
from dataclasses import dataclass
from typing import Self
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import args, scope, val


@dataclass(frozen=True)
class AbstractClass(val.Val):
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def create(self, *args, **kwargs) -> "object_.Object":
        ...

    def __call__(self, scope: scope.Scope, args: args.Args) -> val.Val:
        instance = self.create()
        if "__init__" in instance:
            instance["__init__"](scope, args)
        elif len(args) > 0:
            raise self._error(
                msg=f"unable to apply init args {args} to instance {instance}"
            )
        return instance


from pysh.pype.vals.classes import object_
