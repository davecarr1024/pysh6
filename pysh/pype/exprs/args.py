from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import arg
from pysh.pype.vals import args, scope


@dataclass(frozen=True)
class Args(Sized, Iterable[arg.Arg]):
    _args: Sequence[arg.Arg] = field(default_factory=list[arg.Arg])

    def __str__(self) -> str:
        return f'({", ".join(map(str,self))})'

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self) -> Iterator[arg.Arg]:
        return iter(self._args)

    def eval(self, scope: scope.Scope) -> args.Args:
        return args.Args([arg.eval(scope) for arg in self])

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Args"]:
        return (
            r"\("
            & (arg.Arg.parser_rule() & (r"," & arg.Arg.parser_rule()).zero_or_more())
            .convert(Args)
            .zero_or_one()
            & r"\)"
        ).convert(lambda args: args or Args())
