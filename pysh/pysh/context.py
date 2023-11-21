from dataclasses import dataclass
from pysh.pysh import vals


@dataclass(frozen=True)
class Context:
    scope: vals.Scope
