from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope
from pysh.pype.statements import result, statement


@dataclass(frozen=True)
class Block(
    statement.Statement,
    Sized,
    Iterable[statement.Statement],
):
    _statements: Sequence[statement.Statement] = field(
        default_factory=list[statement.Statement]
    )

    def __len__(self) -> int:
        return len(self._statements)

    def __iter__(self) -> Iterator[statement.Statement]:
        return iter(self._statements)

    def __str__(self) -> str:
        return f'{{\n{"".join(f"  {statement}" for statement in self)}\n}}'

    def eval(self, scope: scope.Scope) -> result.Result:
        scope = scope.as_child()
        for statement_ in self:
            try:
                result_ = statement_.eval(scope)
            except core.errors.Error as error:
                raise self._error(children=[error])
            if result_.is_return():
                return result_
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Block"]:
        return ("{" & statement.Statement.ref().zero_or_more() & "}").convert(Block)
