from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True, repr=False)
class Error(Exception):
    msg: Optional[str] = None

    def _repr_line(self) -> str:
        return f"{type(self)}(msg={repr(self.msg)})"

    def _repr(self, indent: int) -> str:
        return f'\n{"  "*indent}{self._repr_line()}'

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self._repr(0)
