from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pysh import state
from pysh.pysh.vals import args, param


@dataclass(frozen=True)
class Params(
    core.errors.Errorable["Params"],
    Sized,
    Iterable[param.Param],
):
    _params: Sequence[param.Param] = field(default_factory=list)

    def __str__(self) -> str:
        return f'({", ".join(map(str,self))})'

    def __len__(self) -> int:
        return len(self._params)

    def __iter__(self) -> Iterator[param.Param]:
        return iter(self._params)

    def bind(self, state: state.State, args: args.Args) -> state.State:
        if len(self) != len(args):
            raise self._error(
                msg=f"expected {len(self)} args but got {len(args)} {args}"
            )
        state = state.as_child()
        for param, arg in zip(self, args):
            self._try(
                lambda: param.bind(state, arg),
                f"binding param {param} to arg {arg}",
            )
        return state
