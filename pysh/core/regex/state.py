from dataclasses import dataclass

from pysh.core.chars import stream


@dataclass(frozen=True)
class State:
    chars: stream.Stream
