from dataclasses import dataclass
from .. import errors
from . import error


@dataclass(kw_only=True)
class NaryError(error.Error, errors.NaryError):
    ...
