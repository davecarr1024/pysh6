from dataclasses import dataclass
from pysh.core.errors import error


@dataclass(kw_only=True, repr=False)
class UnaryError(error.Error):
    child: error.Error

    def _repr(self, indent: int) -> str:
        return super()._repr(indent) + self.child._repr(indent + 1)
