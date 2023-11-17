from dataclasses import dataclass
from typing import Optional
from pysh.pype.vals import builtins, val


@dataclass(frozen=True)
class Result:
    return_value: Optional[val.Val] = None

    def is_return(self) -> bool:
        return self.return_value is not None

    @staticmethod
    def for_return(value: Optional[val.Val] = None) -> "Result":
        return Result(value if value is not None else builtins.none)
