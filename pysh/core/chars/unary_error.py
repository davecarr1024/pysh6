from dataclasses import dataclass
from .. import errors
from . import error


@dataclass(kw_only=True)
class UnaryError(error.Error, errors.UnaryError):
    ...
