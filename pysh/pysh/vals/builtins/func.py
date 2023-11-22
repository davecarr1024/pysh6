from dataclasses import dataclass
from pysh.pysh.vals import type


@dataclass(frozen=True)
class _Func(type.Type):
    @property
    def name(self) -> str:
        return "func"


func_ = _Func()
