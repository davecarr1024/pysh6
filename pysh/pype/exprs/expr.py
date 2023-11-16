from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence, Type
from pysh import core
from pysh.pype import parser

_scope_getter = core.parser.states.StateValueGetter[
    parser.Parser, core.parser.rules.Scope[parser.Parser, "Expr"]
].load(lambda parser: parser.expr_scope)


@dataclass(frozen=True)
class Expr(core.parser.Parsable[parser.Parser, "Expr"]):
    @classmethod
    def types(cls) -> Sequence[Type["Expr"]]:
        return [cls, literal.Literal, ref.Ref]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Expr"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, scope: "scope.Scope") -> "val.Val":
        ...

    def _error(
        self,
        *,
        msg: Optional[str] = None,
        children: Sequence[core.errors.Error] = [],
    ) -> "error.Error":
        return error.Error(
            expr=self,
            msg=msg,
            _children=children,
        )


from pysh.pype.exprs import error, literal
from pysh.pype.exprs.ref import ref
from pysh.pype.vals import scope, val
