from dataclasses import dataclass
from typing import Generic
from pysh.core.errors import child_error, error


@dataclass(kw_only=True, repr=False)
class UnaryError(error.Error, Generic[child_error.ChildError]):
    child: child_error.ChildError

    def _repr(self, indent: int) -> str:
        return super()._repr(indent) + self.child._repr(indent + 1)
