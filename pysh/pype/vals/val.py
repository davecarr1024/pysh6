from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, MutableMapping, Optional, Sequence, Type
from pysh import core


@dataclass(
    frozen=True,
    kw_only=True,
)
class Val(MutableMapping[str, "Val"]):
    members: "scope.Scope" = field(default_factory=lambda: scope.Scope())

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule["parser.Parser", "Val"]:
        return int_.Int.parser_rule()

    def __call__(self, scope: "scope.Scope", args: "args.Args") -> "Val":
        raise self._error(msg="uncallable val")

    def _error(
        self,
        *,
        msg: Optional[str] = None,
        children: Sequence[core.errors.Error] = [],
    ) -> "error.Error":
        return error.Error(
            val=self,
            msg=msg,
            _children=children,
        )

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self) -> Iterator[str]:
        return iter(self.members)

    def __getitem__(self, name: str) -> "Val":
        if name not in self.members:
            raise self._error(msg=f"unknown member {name}")
        return self.members[name]

    def __setitem__(self, name: str, val: "Val") -> None:
        self.members[name] = val

    def __delitem__(self, name: str) -> None:
        del self.members[name]

    def can_bind(self) -> bool:
        return False

    def bind(self, obj: "Val") -> "Val":
        raise self._error(msg="trying to bind unbindable val")


from pysh.pype import parser
from pysh.pype.vals import args, error, scope
from pysh.pype.vals.builtins import int_
