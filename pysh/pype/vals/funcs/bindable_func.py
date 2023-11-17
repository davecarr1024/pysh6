from dataclasses import dataclass
from pysh.pype.vals import val
from pysh.pype.vals.funcs import abstract_func, bound_func


@dataclass(
    frozen=True,
    kw_only=True,
)
class BindableFunc(val.Val):
    func: abstract_func.AbstractFunc

    def can_bind(self) -> bool:
        return True

    def bind(self, obj: val.Val) -> val.Val:
        return bound_func.BoundFunc(
            func=self.func,
            obj=obj,
        )
