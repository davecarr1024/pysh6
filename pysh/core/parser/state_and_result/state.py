from dataclasses import dataclass
from pysh.core import tokens


@dataclass(frozen=True)
class State:
    tokens: tokens.Stream
