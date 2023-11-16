from dataclasses import dataclass
from pysh.pype.vals import scope
from pysh.pype.vals.builtins import class_, object_


@dataclass(frozen=True)
class None_(object_.Object):
    ...


none_class = class_.Class(
    _name="None",
    _object_type=None_,
    members=scope.Scope(),
)

none = none_class.create()
