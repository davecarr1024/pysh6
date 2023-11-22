from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type
from pysh import core
from pysh.pysh import state
from pysh.pysh.statements import result


@dataclass(frozen=True)
class Statement(
    core.errors.Errorable["Statement"],
    core.parser.Parsable["parser.Parser", "Statement"],
):
    def __str__(self) -> str:
        return self._str(0)

    def _str(self, indent: int) -> str:
        return f'{"  "*indent}{self._str_line()}'

    def _str_line(self) -> str:
        return repr(self)

    @classmethod
    def types(cls) -> Sequence[Type["Statement"]]:
        return [
            cls,
            assignment.Assignment,
            block.Block,
            decl.Decl,
            empty.Empty,
            func.Func,
            literal.Literal,
            return_.Return,
        ]

    @classmethod
    def scope_getter(
        cls,
    ) -> core.parser.states.StateValueGetter[
        "parser.Parser", core.parser.rules.Scope["parser.Parser", "Statement"]
    ]:
        return _scope_getter

    @abstractmethod
    def eval(self, state: state.State) -> result.Result:
        ...


_scope_getter = core.parser.states.StateValueGetter[
    "parser.Parser", core.parser.rules.Scope["parser.Parser", "Statement"]
].load(lambda parser: parser.statement_scope)

from pysh.pysh import parser
from . import assignment, block, decl, empty, func, literal, return_
