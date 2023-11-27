from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pysp import parser


@dataclass(frozen=True)
class Val(
    core.parser.Parsable[parser.Parser, "Val"],
    core.errors.Errorable["Val"],
):
    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [cls, func.Func, int_.Int, str_.Str]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Val"]
    ]:
        return core.parser.states.StateValueGetter[
            parser.Parser, core.parser.rules.Scope[parser.Parser, Val]
        ].load(lambda state: state.val_scope)

    def apply(self, args: Sequence["Val"], scope: "scope.Scope") -> "Val":
        raise self._error(msg="trying to apply unapplyable val")


from pysh.pysp import func, int_, scope, str_
