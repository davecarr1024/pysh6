from dataclasses import dataclass
from pysh import core
from pysh.pysh import state
from pysh.pysh.vals import arg, var, type


@dataclass(frozen=True)
class Param(core.errors.Errorable["Param"]):
    type: type.Type
    name: str

    def __str__(self) -> str:
        return f"{self.name}: {self.type}"

    def bind(self, state: state.State, arg: arg.Arg) -> None:
        self._try(
            lambda: state.__setitem__(self.name, var.Var(self.type, arg.val)),
            f"bind {arg}",
        )
