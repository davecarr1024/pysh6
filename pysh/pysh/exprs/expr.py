from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core

_scope_getter = core.parser.states.StateValueGetter[
    "parser.Parser", core.parser.rules.Scope["parser.Parser", "Expr"]
].load(lambda parser: parser.expr_scope)


@dataclass(frozen=True)
class Expr(
    core.errors.Errorable["Expr"],
    core.parser.Parsable["parser.Parser", "Expr"],
):
    @classmethod
    def types(cls) -> Sequence[Type["Expr"]]:
        return [cls, ref.Ref]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        "parser.Parser", core.parser.rules.Scope["parser.Parser", "Expr"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, state: "state.State") -> "val.Val":
        ...


from pysh.pysh.vals import val
from pysh.pysh import parser, state
from . import ref
