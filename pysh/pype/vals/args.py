from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import arg


@dataclass(frozen=True)
class Args(Iterable[arg.Arg], Sized):
    _vals: Sequence[arg.Arg] = field(default_factory=list[arg.Arg])

    def __len__(self) -> int:
        return len(self._vals)

    def __iter__(self) -> Iterator[arg.Arg]:
        return iter(self._vals)
