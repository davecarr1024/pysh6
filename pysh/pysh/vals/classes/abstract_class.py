from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from pysh.pysh.vals import scope, type


@dataclass(frozen=True)
class AbstractClass(type.Type):
    _name: str
    _members: scope.Scope = field(default_factory=scope.Scope)
    _parent: Optional["AbstractClass"] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def members(self) -> scope.Scope:
        return self._members

    @property
    def parent(self) -> Optional["AbstractClass"]:
        return self._parent

    @abstractmethod
    def create(self, *args, **kwargs) -> "object_.Object":
        ...


from . import object_
