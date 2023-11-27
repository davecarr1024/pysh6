from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence, Type
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope
from pysh.pype.statements import result

_scope_getter = core.parser.states.StateValueGetter[
    parser.Parser, core.parser.rules.Scope[parser.Parser, "Statement"]
].load(lambda parser: parser.statement_scope)


@dataclass(frozen=True)
class Statement(
    core.parser.Parsable[parser.Parser, "Statement"],
    core.errors.Errorable["Statement"],
):
    @classmethod
    def types(cls) -> Sequence[Type["Statement"]]:
        return [
            cls,
            assignment.Assignment,
            block.Block,
            class_.Class,
            empty.Empty,
            func.Func,
            expr_statement.ExprStatement,
            return_.Return,
        ]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Statement"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, scope: scope.Scope) -> result.Result:
        ...


from pysh.pype.statements import (
    assignment,
    block,
    class_,
    empty,
    expr_statement,
    func,
    result,
    return_,
)
