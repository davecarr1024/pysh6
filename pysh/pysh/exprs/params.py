from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized
from pysh import core
from pysh.pysh import parser, state
from pysh.pysh.exprs import param
from pysh.pysh.vals import params


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

    def bind(self, state: state.State) -> params.Params:
        return params.Params([param.bind(state) for param in self])

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
