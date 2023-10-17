from dataclasses import dataclass, field
from pysh.core import tokens


@dataclass(frozen=True)
class State:
    tokens_: tokens.Stream = field(default_factory=tokens.Stream)
