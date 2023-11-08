from dataclasses import dataclass
from pysh.core import chars


@dataclass(frozen=True)
class State:
    chars: chars.Stream
