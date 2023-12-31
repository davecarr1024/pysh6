from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pysp import parser, scope, val


@dataclass(frozen=True)
class Expr(core.parser.Parsable[parser.Parser, "Expr"]):
    @classmethod
    def types(cls) -> Sequence[Type["Expr"]]:
        return [
            cls,
            call.Call,
            decl.Decl,
            literal.Literal,
            ref.Ref,
        ]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Expr"]
    ]:
        return core.parser.states.StateValueGetter[
            parser.Parser, core.parser.rules.Scope[parser.Parser, "Expr"]
        ].load(lambda parser: parser.expr_scope)

    @abstractmethod
    def eval(self, scope: scope.Scope) -> val.Val:
        ...


from pysh.pysp import call, decl, literal, ref
