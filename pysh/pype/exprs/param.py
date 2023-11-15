from dataclasses import dataclass
from pysh.pype import vals


@dataclass(frozen=True)
class Param:
    name: str

    def eval(self, arg: vals.Arg, scope: vals.Scope) -> None:
        scope[self.name] = arg.val
