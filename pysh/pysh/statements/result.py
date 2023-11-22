from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Result:
    return_value: Optional["val.Val"] = field(default_factory=lambda: none_.none)

    @property
    def is_return(self) -> bool:
        return self.return_value is not None

    @staticmethod
    def for_return(return_value: Optional["val.Val"] = None) -> "Result":
        return Result(return_value or none_.none)


from pysh.pysh.vals import val
from pysh.pysh.vals.builtins import none_
