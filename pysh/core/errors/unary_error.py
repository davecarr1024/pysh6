from dataclasses import dataclass
from . import error


@dataclass(frozen=True, kw_only=True)
class UnaryError(error.Error):
    child: error.Error
