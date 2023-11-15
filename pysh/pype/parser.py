from dataclasses import dataclass
from pysh import core


@dataclass(frozen=True)
class Parser(core.parser.states.State):
    ...
