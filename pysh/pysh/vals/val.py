from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Mapping
from pysh import core


@dataclass(frozen=True)
class Val(
    ABC,
    core.errors.Errorable["Val"],
    Mapping[str, "var.Var"],
):
    @property
    @abstractmethod
    def type(self) -> "type.Type":
        ...

    @property
    def members(self) -> "scope.Scope":
        return scope.Scope()

    def __call__(self, scope: "scope.Scope", args: "args.Args") -> "Val":
        raise self._error(msg="uncallable")

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self) -> Iterator[str]:
        return iter(self.members)

    def __getitem__(self, name: str) -> "var.Var":
        return self._try(lambda: self.members[name])

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule["parser.Parser", "Val"]:
        return builtins.Int.parser_rule()


from pysh.pysh import parser
from . import args, builtins, scope, var
from . import type
