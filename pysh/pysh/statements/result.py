from dataclasses import dataclass
from typing import Optional

from pysh.pysh import vals


@dataclass(frozen=True)
class Result:
    return_value: Optional[vals.Val] = vals.none

    @property
    def is_return(self) -> bool:
        return self.return_value is not None

    @staticmethod
    def for_return(return_value: vals.Val = vals.none) -> "Result":
        return Result(return_value)
