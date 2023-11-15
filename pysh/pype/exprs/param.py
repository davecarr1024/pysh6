from dataclasses import dataclass
from pysh.pype import vals


@dataclass(frozen=True)
class Param:
    name: str
