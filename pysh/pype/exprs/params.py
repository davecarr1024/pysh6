from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh.pype import error
from pysh.pype.vals import args, scope
from pysh.pype.exprs import param


@dataclass(frozen=True)
class Params(Sized, Iterable[param.Param]):
    _params: Sequence[param.Param] = field(default_factory=list[param.Param])

    def __len__(self) -> int:
        return len(self._params)

    def __iter__(self) -> Iterator[param.Param]:
        return iter(self._params)

    def bind(self, args: args.Args, scope: scope.Scope) -> scope.Scope:
        if len(self) != len(args):
            raise error.Error(
                msg=f"param count mismatch expected {len(self)} got {len(args)}"
            )
        return scope.as_child({param.name: arg.val for param, arg in zip(self, args)})

    def tail(self) -> "Params":
        if len(self) == 0:
            raise error.Error(msg=f"unable to get tail of empty params {self}")
        return Params(self._params[1:])
