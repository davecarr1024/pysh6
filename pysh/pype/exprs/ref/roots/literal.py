from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val
from pysh.pype.exprs.ref.roots import root


@dataclass(frozen=True)
class Literal(root.Root):
    value: val.Val

    def __str__(self) -> str:
        return str(self.value)

    def eval(self, scope: scope.Scope) -> "val.Val":
        return self.value

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Literal"]:
        return val.Val.ref().convert(Literal)
