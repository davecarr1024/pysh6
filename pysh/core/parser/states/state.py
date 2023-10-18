from dataclasses import dataclass, field
from pysh.core import tokens as tokens_lib


@dataclass(frozen=True)
class State:
    tokens: tokens_lib.Stream = field(default_factory=tokens_lib.Stream)
