from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pysp import parser


@dataclass(frozen=True)
class Val(core.parser.Parsable[parser.Parser, "Val"]):
    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [cls, int_.Int, str_.Str]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Val"]
    ]:
        return core.parser.states.StateValueGetter[
            parser.Parser, core.parser.rules.Scope[parser.Parser, Val]
        ].load(lambda state: state.val_scope)


from pysh.pysp import int_, str_
