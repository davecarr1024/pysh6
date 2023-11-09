from dataclasses import dataclass, field
from typing import Optional
from pysh.core import chars as chars_lib


@dataclass(frozen=True)
class State:
    chars: chars_lib.Stream = field(default_factory=chars_lib.Stream)

    @staticmethod
    def load(value: str, position: Optional[chars_lib.Position] = None) -> "State":
        return State(chars_lib.Stream.load(value, position))
