from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pype import parser, vals

_scope_getter = core.parser.states.StateValueGetter[
    parser.Parser, core.parser.rules.Scope[parser.Parser, "Statement"]
].load(lambda parser: parser.statement_scope)


@dataclass(frozen=True)
class Statement(core.parser.Parsable[parser.Parser, "Statement"]):
    @classmethod
    def types(cls) -> Sequence[Type["Statement"]]:
        return [cls, expr_statement.ExprStatement]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Statement"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, scope: vals.Scope) -> None:
        ...


from pysh.pype.statements import expr_statement
