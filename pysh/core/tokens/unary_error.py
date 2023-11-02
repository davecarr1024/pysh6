from dataclasses import dataclass
from pysh.core import errors
from pysh.core.tokens import error


@dataclass(kw_only=True, repr=False)
class UnaryError(error.Error, errors.UnaryError):
    ...
