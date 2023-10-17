from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    line: int = 0
    column: int = 0

    def __add__(self, char: "char.Char") -> "Position":
        if char.value == "\n":
            return Position(self.line + 1, 0)
        else:
            return Position(self.line, self.column + 1)


from pysh.core.chars import char
