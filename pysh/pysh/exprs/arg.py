from dataclasses import dataclass
from pysh import core
from pysh.pysh import state
from pysh.pysh.exprs import expr
from pysh.pysh.vals import arg


@dataclass(frozen=True)
class Arg(core.errors.Errorable["Arg"]):
    val: expr.Expr

    def __str__(self) -> str:
        return str(self.val)

    def bind(self, state: state.State) -> arg.Arg:
        return self._try(
            lambda: arg.Arg(self.val.eval(state)),
            "binding arg expr",
        )
