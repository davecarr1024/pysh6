from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pype import parser, vals

_scope_getter = core.parser.states.StateValueGetter[
    parser.Parser, core.parser.rules.Scope[parser.Parser, "Expr"]
].load(lambda parser: parser.expr_scope)


@dataclass(frozen=True)
class Expr(core.parser.Parsable[parser.Parser, "Expr"]):
    @classmethod
    def types(cls) -> Sequence[Type["Expr"]]:
        return [cls, literal.Literal]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Expr"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, scope: vals.Scope) -> vals.Val:
        ...


from pysh.pype.exprs import literal
