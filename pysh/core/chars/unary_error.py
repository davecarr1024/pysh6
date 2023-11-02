from dataclasses import dataclass
from pysh.core import errors
from pysh.core.chars import error


@dataclass(kw_only=True, repr=False)
class UnaryError(error.Error, errors.UnaryError):
    ...
