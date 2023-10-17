from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import error


@dataclass(kw_only=True)
class NaryError(error.Error, errors.NaryError):
    ...
