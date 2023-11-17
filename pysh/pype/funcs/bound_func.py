from dataclasses import dataclass
from pysh import core
from pysh.pype.vals import args, scope, val
from pysh.pype.funcs import abstract_func


@dataclass(
    frozen=True,
    kw_only=True,
)
class BoundFunc(abstract_func.AbstractFunc):
    func: abstract_func.AbstractFunc
    obj: val.Val

    def name(self) -> str:
        return self.func.name()

    def __call__(
        self,
        scope: scope.Scope,
        args: args.Args,
    ) -> val.Val:
        try:
            return self.func(scope, args.prepend(self.obj))
        except core.errors.Error as error:
            raise self._error(children=[error])
