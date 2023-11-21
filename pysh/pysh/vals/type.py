from dataclasses import dataclass
from typing import Iterator, Optional
from pysh.pysh.vals import val


@dataclass(frozen=True)
class Type(val.Val):
    @property
    def type(self) -> "Type":
        return builtin_type

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def parent(self) -> Optional["Type"]:
        return None

    @property
    def ancestors(self) -> Iterator["Type"]:
        type: Optional[Type] = self
        while type is not None:
            yield type
            type = type.parent

    def assert_can_assign(self, rhs: "Type") -> None:
        if self not in rhs.ancestors:
            raise self._error(
                msg=f"can't assign from rhs {rhs}: not in ancestors {rhs.ancestors}"
            )


from pysh.pysh.vals.builtins import builtin_type
