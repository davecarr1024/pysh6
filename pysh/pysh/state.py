from dataclasses import dataclass
from pysh.pysh import vals


@dataclass(frozen=True)
class State:
    scope: vals.Scope
