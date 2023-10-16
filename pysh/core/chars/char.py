from dataclasses import dataclass, field
from .. import errors


@dataclass(frozen=True)
class Char:
    value: str
    position: "position.Position" = field(default_factory=lambda: position.Position())

    def __post_init__(self):
        if len(self.value) != 1:
            raise errors.Error(msg=f"invalid char {self}")


from . import position
