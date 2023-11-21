from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pysh import parser
from pysh.pysh.vals import arg


@dataclass(frozen=True)
class Args(Sized, Iterable[arg.Arg]):
    _args: Sequence[arg.Arg] = field(default_factory=list)

    def __str__(self) -> str:
        return f'({", ".join(map(str,self))})'

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self) -> Iterator[arg.Arg]:
        return iter(self._args)

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Args"]:
        return (
            r"\("
            & (arg.Arg.parser_rule() & ("," & arg.Arg.parser_rule()).zero_or_more())
            .convert(Args)
            .zero_or_one()
            .convert(lambda args: args or Args())
            & r"\)"
        )
