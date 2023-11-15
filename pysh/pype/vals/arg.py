from dataclasses import dataclass
from pysh.pype.vals import val


@dataclass(frozen=True)
class Arg:
    val: val.Val
