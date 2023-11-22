from dataclasses import dataclass, field
from typing import Generic, TypeVar
from pysh.pysh.vals.classes import abstract_object

_Object = TypeVar("_Object", bound="Object")


@dataclass(frozen=True)
class Object(
    abstract_object.AbstractObject,
    Generic[_Object],
):
    _class: "class_.Class[_Object]" = field(repr=False)

    @property
    def type(self) -> "class_.Class[_Object]":
        return self._class


from . import class_
