from dataclasses import dataclass, field
from typing import Iterator, Mapping, MutableMapping, Optional
from pysh import core


@dataclass(frozen=True)
class Scope(
    core.errors.Errorable["Scope"],
    MutableMapping[str, "var.Var"],
):
    _vars: MutableMapping[str, "var.Var"] = field(default_factory=dict)
    parent: Optional["Scope"] = None

    @property
    def vars(self) -> Mapping[str, "var.Var"]:
        return self._vars

    @property
    def _all_vars(self) -> Mapping[str, "var.Var"]:
        return (
            dict(self.parent._all_vars) | dict(self._vars)
            if self.parent is not None
            else self._vars
        )

    def __len__(self) -> int:
        return len(self._all_vars)

    def __iter__(self) -> Iterator[str]:
        return iter(self._all_vars)

    def __getitem__(self, name: str) -> "var.Var":
        if name in self._vars:
            return self._vars[name]
        elif self.parent is not None:
            return self.parent[name]
        else:
            raise self._error(msg=f"unknown var {name}")

    def __setitem__(self, name: str, var: "var.Var") -> None:
        self._vars[name] = var

    def __delitem__(self, name: str) -> None:
        self._try(lambda: self._vars.__delitem__(name))

    def as_child(self, vars: MutableMapping[str, "var.Var"] = {}) -> "Scope":
        return Scope(vars, self)


from . import var
