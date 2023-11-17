from dataclasses import dataclass
from pysh.pype.vals import val


@dataclass(
    frozen=True,
    kw_only=True,
)
class AbstractFunc(val.Val):
    name: str
