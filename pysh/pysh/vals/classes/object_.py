from dataclasses import dataclass
from pysh.pysh.vals import args, scope, val


@dataclass(frozen=True)
class Object(val.Val):
    _class: "abstract_class.AbstractClass"
    _members: scope.Scope

    @property
    def type(self) -> "abstract_class.AbstractClass":
        return self._class

    @property
    def members(self) -> scope.Scope:
        return self._members

    def __call__(self, scope: scope.Scope, args: args.Args) -> val.Val:
        return self._try(
            lambda: self["__call__"].val(scope, args),
            "failed to call object's __call__",
        )


from . import abstract_class
