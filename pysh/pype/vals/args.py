from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh.pype.vals import arg


@dataclass(frozen=True)
class Args(Iterable[arg.Arg], Sized):
    _args: Sequence[arg.Arg] = field(default_factory=list[arg.Arg])

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self) -> Iterator[arg.Arg]:
        return iter(self._args)

    def prepend(self, obj: "val.Val") -> "Args":
        return Args([arg.Arg(obj)] + list(self._args))


from pysh.pype.vals import val
