from dataclasses import dataclass, field

from pysh.pype.vals.classes import abstract_class, object_


@dataclass(frozen=True)
class Class(abstract_class.AbstractClass):
    _name: str = field(kw_only=True)

    def name(self) -> str:
        return self._name

    def create(self, *args, **kwargs) -> object_.Object:
        obj = object_.Object(
            members=self.members.as_child(),
            class_=self,
        )
        obj.members.bind(obj)
        return obj
