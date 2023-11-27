from dataclasses import dataclass, field
from pysh.core import errors


@dataclass(frozen=True)
class Char(errors.Errorable["Char"]):
    value: str
    position: "position.Position" = field(default_factory=lambda: position.Position())

    def __post_init__(self):
        if len(self.value) != 1:
            raise self._error(msg=f"invalid char value len {len(self.value)}")


from pysh.core.chars import position
