from dataclasses import dataclass, field
from typing import Iterator, Mapping, MutableMapping, Optional
from pysh.pysp import error, val


@dataclass(frozen=True)
class Scope(MutableMapping[str, val.Val]):
    _vals: MutableMapping[str, val.Val] = field(default_factory=dict[str, val.Val])
    _parent: Optional["Scope"] = None

    def __str__(self) -> str:
        return str(self.all_vals())

    def __len__(self) -> int:
        return len(self.all_vals())

    def __iter__(self) -> Iterator[str]:
        return iter(self.all_vals())

    def __getitem__(self, name: str) -> val.Val:
        if name in self._vals:
            return self._vals[name]
        elif self._parent is not None:
            return self._parent[name]
        else:
            raise error.Error(msg=f"unknown val {name}")

    def __delitem__(self, name: str) -> None:
        del self._vals[name]

    def __setitem__(self, name: str, value: val.Val) -> None:
        self._vals[name] = value

    def all_vals(self) -> Mapping[str, val.Val]:
        return (
            dict(self._parent.all_vals()) | dict(self)
            if self._parent is not None
            else self
        )
