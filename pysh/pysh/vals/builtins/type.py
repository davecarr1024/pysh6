from dataclasses import dataclass
from pysh.pysh.vals import type as type_lib


@dataclass(frozen=True)
class _Type(type_lib.Type):
    ...


type_ = _Type()
