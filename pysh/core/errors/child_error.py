from typing import TypeVar
from pysh.core.errors import error

ChildError = TypeVar("ChildError", bound=error.Error, covariant=True)
