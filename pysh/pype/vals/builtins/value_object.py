from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.pype.vals.builtins import object_

_Value = TypeVar("_Value")


@dataclass(
    frozen=True,
    kw_only=True,
)
class ValueObject(
    object_.Object,
    Generic[_Value],
):
    value: _Value
