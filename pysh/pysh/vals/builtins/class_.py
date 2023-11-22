from dataclasses import dataclass
from typing import Generic, Optional, Type, TypeVar
from pysh.pysh.vals.classes import abstract_class

_Object = TypeVar("_Object", bound="object_.Object")


@dataclass(frozen=True)
class Class(
    abstract_class.AbstractClass,
    Generic[_Object],
):
    _obj_type: Type[_Object]
    _name: Optional[str] = None

    @property
    def name(self) -> str:
        return self._name or self._obj_type.__name__

    def create(self, *args, **kwargs) -> _Object:
        return self._obj_type(
            self,
            *args,
            **kwargs,
        )


from . import object_
