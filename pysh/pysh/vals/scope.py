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

    def __str__(self) -> str:
        def _str_var(name: str, var: var.Var) -> str:
            return (
                f"{name}: {var.type} = {var.val}"
                if var.initialized
                else f"{name}: {var.type}"
            )

        return f'{{{", ".join(_str_var(name,var) for name, var in self.items())}}}'

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

    def __or__(self, rhs: "Scope") -> "Scope":
        return Scope(dict(self) | dict(rhs))

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and (
            name in self._vars or (self.parent is not None and name in self.parent)
        )

    def as_child(
        self, vars: Optional[MutableMapping[str, "var.Var"]] = None
    ) -> "Scope":
        return Scope(
            vars if vars is not None else {},
            self,
        )


from . import var
