from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val
from pysh.pype.exprs.refs.roots import root


@dataclass(frozen=True)
class Literal(root.Root):
    value: val.Val

    def __str__(self) -> str:
        return str(self.value)

    def get(self, scope: scope.Scope) -> "val.Val":
        return self.value

    def set(self, scope: scope.Scope, val: val.Val) -> None:
        raise self._error(msg="unable to set literal ref")

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Literal"]:
        return val.Val.parser_rule().convert(Literal)
