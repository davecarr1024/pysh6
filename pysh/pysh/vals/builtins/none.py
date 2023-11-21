from dataclasses import dataclass
from pysh.pysh.vals.classes import abstract_class
from pysh.pysh.vals import type, val


@dataclass(frozen=True)
class _None(val.Val):
    @property
    def type(self) -> "type.Type":
        return none_class


none_class = abstract_class.AbstractClass("none")
none = _None()
