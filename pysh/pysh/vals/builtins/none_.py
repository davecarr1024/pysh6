from dataclasses import dataclass
from . import class_, object_


@dataclass(frozen=True)
class _None(object_.Object["_None"]):
    @property
    def type(self) -> class_.Class:
        return none_class


none_class = class_.Class(_None, "None")
none = none_class.create()
