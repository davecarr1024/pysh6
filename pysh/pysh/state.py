from dataclasses import dataclass, field
from typing import Iterator, MutableMapping, Optional

from pysh import core


@dataclass(frozen=True)
class State(
    core.errors.Errorable["State"],
    MutableMapping[str, "var.Var"],
):
    scope: "scope_lib.Scope" = field(
        default_factory=lambda: State._default_scope(),
    )

    def __str__(self) -> str:
        return str(self.scope)

    @staticmethod
    def _default_scope() -> "scope_lib.Scope":
        return scope_lib.Scope(
            {
                "int": var.Var.for_val(builtins.int_class),
                "none": var.Var.for_val(builtins.none),
            }
        )

    def __or__(self, rhs: "State") -> "State":
        return State(self.scope | rhs.scope)

    def __len__(self) -> int:
        return len(self.scope)

    def __iter__(self) -> Iterator[str]:
        return iter(self.scope)

    def __getitem__(self, name: str) -> "var.Var":
        return self._try(
            lambda: self.scope[name],
            msg=f"get {name}",
        )

    def __setitem__(self, name: str, var: "var.Var") -> None:
        self._try(
            lambda: self.scope.__setitem__(name, var),
            msg=f"set {name} = {var}",
        )

    def __delitem__(self, name: str) -> None:
        self._try(lambda: self.scope.__delitem__(name))

    def __contains__(self, name: object) -> bool:
        return name in self.scope

    def as_child(
        self, vars: Optional[MutableMapping[str, "var.Var"]] = None
    ) -> "State":
        return State(self.scope.as_child(vars))


from .vals import builtins, scope as scope_lib, var
