from dataclasses import dataclass, field
from typing import Sequence
from . import error


@dataclass(kw_only=True, repr=False)
class NaryError(error.Error):
    children: Sequence[error.Error] = field(default_factory=list[error.Error])

    def _repr(self, indent: int) -> str:
        s: str = super()._repr(indent)
        for child in self.children:
            s += child._repr(indent + 1)
        return s
