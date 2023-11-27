from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import args, scope
from pysh.pype.exprs import param


@dataclass(frozen=True)
class Params(
    Sized,
    Iterable[param.Param],
    core.errors.Errorable["Params"],
):
    _params: Sequence[param.Param] = field(default_factory=list[param.Param])

    def __len__(self) -> int:
        return len(self._params)

    def __iter__(self) -> Iterator[param.Param]:
        return iter(self._params)

    def bind(self, args: args.Args, scope: scope.Scope) -> scope.Scope:
        if len(self) != len(args):
            raise self._error(
                msg=f"param count mismatch expected {len(self)} got {len(args)}"
            )
        return scope.as_child({param.name: arg.val for param, arg in zip(self, args)})

    def tail(self) -> "Params":
        if len(self) == 0:
            raise self._error(msg=f"unable to get tail of empty params")
        return Params(self._params[1:])

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Params"]:
        return (
            r"\("
            & (
                param.Param.parser_rule()
                & ("," & param.Param.parser_rule()).zero_or_more()
            )
            .convert(Params)
            .zero_or_one()
            & r"\)"
        ).convert(lambda params: params or Params())
