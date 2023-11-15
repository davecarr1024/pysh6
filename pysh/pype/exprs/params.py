from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh.pype import error, vals
from pysh.pype.exprs import param


@dataclass(frozen=True)
class Params(Sized, Iterable[param.Param]):
    _params: Sequence[param.Param] = field(default_factory=list[param.Param])

    def __len__(self) -> int:
        return len(self._params)

    def __iter__(self) -> Iterator[param.Param]:
        return iter(self._params)

    def eval(self, args: vals.Args, scope: vals.Scope) -> vals.Scope:
        if len(self) != len(args):
            raise error.Error(
                msg=f"param count mismatch expected {len(self)} got {len(args)}"
            )
        scope_ = vals.Scope({}, scope)
        for param, arg in zip(self, args):
            param.eval(arg, scope_)
        return scope_
