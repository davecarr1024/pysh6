from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pysh import parser, state, vals
from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Block(
    statement.Statement,
    Sized,
    Iterable[statement.Statement],
):
    _statements: Sequence[statement.Statement] = field(default_factory=list)

    def _str(self, indent: int) -> str:
        r = f"{'  '*indent}{{\n"
        for statement in self:
            r += f"{statement._str(indent+1)}\n"
        r += f"{'  '*indent}}}\n"
        return r

    def __len__(self) -> int:
        return len(self._statements)

    def __iter__(self) -> Iterator[statement.Statement]:
        return iter(self._statements)

    def eval(self, state: state.State) -> result.Result:
        scope = vals.Scope({}, state.scope)
        for statement in self:
            result_ = self._try(lambda: statement.eval(state))
            if result_.is_return:
                return result_
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Block"]:
        return ("{" & statement.Statement.ref().zero_or_more() & "}").convert(Block)
