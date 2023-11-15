from dataclasses import dataclass
from typing import cast
from pysh.pype import vals
from pysh.pype.vals.builtins import class_, value_object


@dataclass(frozen=True)
class Int(value_object.ValueObject[int]):
    @staticmethod
    def create(value: int) -> "Int":
        return cast(Int, int_class.create(value))


int_class = class_.Class(
    _name="Int",
    _object_type=Int,
    members=vals.Scope(),
)
