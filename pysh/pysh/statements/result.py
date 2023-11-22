from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Result:
    return_value: Optional["val.Val"] = None

    @property
    def is_return(self) -> bool:
        return self.return_value is not None

    @staticmethod
    def for_return(return_value: Optional["val.Val"] = None) -> "Result":
        return Result(return_value if return_value is not None else none_.none)


from pysh.pysh.vals import val
from pysh.pysh.vals.builtins import none_
