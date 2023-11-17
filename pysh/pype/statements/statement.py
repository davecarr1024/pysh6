from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence, Type
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val

_scope_getter = core.parser.states.StateValueGetter[
    parser.Parser, core.parser.rules.Scope[parser.Parser, "Statement"]
].load(lambda parser: parser.statement_scope)


@dataclass(frozen=True)
class Statement(core.parser.Parsable[parser.Parser, "Statement"]):
    @dataclass(frozen=True)
    class Result:
        @dataclass(frozen=True)
        class Return:
            value: Optional[val.Val] = None

        return_: Optional[Return] = None

        def is_return(self) -> bool:
            return self.return_ is not None

        @staticmethod
        def for_return(val: Optional[val.Val] = None) -> "Statement.Result":
            return Statement.Result(Statement.Result.Return(val))

    @classmethod
    def types(cls) -> Sequence[Type["Statement"]]:
        return [
            cls,
            assignment.Assignment,
            class_.Class,
            expr_statement.ExprStatement,
        ]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        parser.Parser, core.parser.rules.Scope[parser.Parser, "Statement"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, scope: scope.Scope) -> "Statement.Result":
        ...

    def _error(
        self,
        *,
        msg: Optional[str] = None,
        children: Sequence[core.errors.Error] = [],
    ) -> "error.Error":
        return error.Error(
            statement=self,
            msg=msg,
            _children=children,
        )


from pysh.pype.statements import assignment, class_, error, expr_statement
