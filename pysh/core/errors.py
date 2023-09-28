from dataclasses import dataclass, field
from typing import Optional, Sequence


@dataclass(frozen=True, kw_only=True)
class Error(Exception):
    msg: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class NaryError(Error):
    children: Sequence[Error] = field(default_factory=list[Error])
