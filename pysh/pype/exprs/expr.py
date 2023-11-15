from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pype import parser, vals


@dataclass(frozen=True)
class Expr(core.parser.Parsable[parser.Parser, "Expr"]):
    @classmethod
    def types(cls) -> Sequence[Type["Expr"]]:
        return [cls]

    @abstractmethod
    def eval(self, scope: vals.Scope) -> vals.Val:
        ...
