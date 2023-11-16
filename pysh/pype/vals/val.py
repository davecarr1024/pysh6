from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, Mapping, Optional, Sequence, Type
from pysh import core

_scope_getter = core.parser.states.StateValueGetter[
    "parser.Parser", core.parser.rules.Scope["parser.Parser", "Val"]
].load(lambda parser: parser.val_scope)


@dataclass(frozen=True)
class Val(
    core.parser.Parsable["parser.Parser", "Val"],
    Mapping[str, "Val"],
):
    members: "scope.Scope" = field(default_factory=lambda: scope.Scope())

    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [cls, int_.Int]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        "parser.Parser", core.parser.rules.Scope["parser.Parser", "Val"]
    ]:
        return _scope_getter

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

    def can_bind(self) -> bool:
        return False

    def bind(self, obj: "Val") -> "Val":
        raise self._error(msg="trying to bind unbindable val")


from pysh.pype import parser
from pysh.pype.vals import args, error, scope
from pysh.pype.vals.builtins import int_
