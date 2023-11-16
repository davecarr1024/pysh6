from dataclasses import dataclass
from pysh import core


@dataclass(kw_only=True, repr=False)
class Error(core.errors.NaryError):
    expr: "expr.Expr"

    def _repr_line(self) -> str:
        return f"ExprError({self.expr},{repr(self.msg)})"


from pysh.pype.exprs import expr
