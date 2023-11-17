from dataclasses import dataclass
from pysh import core
from pysh.pype.vals import val


@dataclass(kw_only=True, repr=False)
class Error(core.errors.NaryError):
    val: val.Val

    def _repr_line(self) -> str:
        return f"ValError({self.val},{repr(self.msg)})"
