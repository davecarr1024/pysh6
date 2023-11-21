from dataclasses import dataclass
from typing import Optional
from pysh import core


@dataclass
class Var(core.errors.Errorable["Var"]):
    type: "type.Type"
    _val: Optional["val.Val"] = None

    @property
    def initialized(self) -> bool:
        return self._val is not None

    @property
    def val(self) -> "val.Val":
        if self._val is None:
            raise self._error(msg="uninitialized var")
        return self._val

    @val.setter
    def val(self, val: "val.Val") -> None:
        self.type.assert_can_assign(val.type)
        self._val = val


from pysh.pysh.vals import type, val
