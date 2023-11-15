from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pype import parser


@dataclass(frozen=True)
class Val(core.parser.Parsable[parser.Parser, "Val"]):
    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [cls]

    @abstractmethod
    def apply(self, args: "args.Args", scope: "scope.Scope") -> "Val":
        ...


from pysh.pype.vals import args, scope
