from dataclasses import dataclass
from typing import Optional, cast
from pysh import core


@dataclass
class Var(core.errors.Errorable["Var"]):
    type: "type.Type"
    _val: Optional["val_lib.Val"] = None

    def __post_init__(self) -> None:
        if self._val is not None:
            self._try(
                lambda: self.type.assert_can_assign(
                    cast(val_lib.Val, self._val).type,
                ),
                msg="invalid var",
            )

    def __str__(self) -> str:
        return f"{self._val}: {self.type}"

    @property
    def initialized(self) -> bool:
        return self._val is not None

    @property
    def val(self) -> "val_lib.Val":
        if self._val is None:
            raise self._error(msg="uninitialized var")
        return self._val

    @val.setter
    def val(self, val: "val_lib.Val") -> None:
        self.type.assert_can_assign(val.type)
        self._val = val

    @staticmethod
    def for_val(val: "val_lib.Val") -> "Var":
        return Var(val.type, val)


from pysh.pysh.vals import type, val as val_lib
