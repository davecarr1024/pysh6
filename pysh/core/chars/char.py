from dataclasses import dataclass, field
from pysh.core.chars import error


@dataclass(frozen=True)
class Char:
    value: str
    position: "position.Position" = field(default_factory=lambda: position.Position())

    def __post_init__(self):
        if len(self.value) != 1:
            raise error.Error(msg=f"invalid char {self}")


from pysh.core.chars import position
