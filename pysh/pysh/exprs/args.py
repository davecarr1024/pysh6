from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pysh import state
from pysh.pysh.exprs import arg
from pysh.pysh.vals import args


@dataclass(frozen=True)
class Args(
    core.errors.Errorable["Args"],
    Sized,
    Iterable[arg.Arg],
):
    _args: Sequence[arg.Arg] = field(default_factory=list)

    def __str__(self) -> str:
        return f'({", ".join(map(str,self))})'

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self) -> Iterator[arg.Arg]:
        return iter(self._args)

    def bind(self, state: state.State) -> args.Args:
        return args.Args([arg.bind(state) for arg in self])
