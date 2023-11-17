from dataclasses import dataclass, field
from typing import Iterator, Mapping, MutableMapping, Optional
from pysh.pype import error


@dataclass(frozen=True)
class Scope(MutableMapping[str, "val.Val"]):
    _vals: MutableMapping[str, "val.Val"] = field(default_factory=dict[str, "val.Val"])
    _parent: Optional["Scope"] = None

    def vals(self) -> Mapping[str, "val.Val"]:
        return (
            dict(self._parent) | dict(self) if self._parent is not None else dict(self)
        )

    def __str__(self) -> str:
        return str(self.vals())

    def __len__(self) -> int:
        return len(self.vals())

    def __iter__(self) -> Iterator[str]:
        return iter(self._vals)

    def __getitem__(self, name: str) -> "val.Val":
        if name in self._vals:
            return self._vals[name]
        elif self._parent is not None:
            return self._parent[name]
        else:
            raise error.Error(msg=f"unknown val {name}")

    def __setitem__(self, name: str, val: "val.Val") -> None:
        self._vals[name] = val

    def __delitem__(self, name: str) -> None:
        del self._vals[name]

    def as_child(self, vals: Mapping[str, "val.Val"] = {}) -> "Scope":
        return Scope(dict(vals), self)

    def bind(self, obj: "val.Val") -> None:
        for name, val in list(self.vals().items()):
            if val.can_bind():
                self[name] = val.bind(obj)


from pysh.pype.vals import val
