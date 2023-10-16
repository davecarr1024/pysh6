from dataclasses import dataclass, field
from typing import Sequence
from . import error


@dataclass(frozen=True, kw_only=True)
class NaryError(error.Error):
    children: Sequence[error.Error] = field(default_factory=list[error.Error])
