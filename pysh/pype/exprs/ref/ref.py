from dataclasses import dataclass, field
from typing import Sequence
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val
from pysh.pype.exprs import expr
from pysh.pype.exprs.ref.parts import part
from pysh.pype.exprs.ref.roots import root


@dataclass(frozen=True)
class Ref(expr.Expr):
    root: root.Root
    parts: Sequence[part.Part] = field(default_factory=list[part.Part])

    def __str__(self) -> str:
        return f'{self.root}{"".join(map(str,self.parts))}'

    def eval(self, scope: scope.Scope) -> val.Val:
        try:
            val = self.root.eval(scope)
            for part in self.parts:
                val = part.eval(scope, val)
            return val
        except core.errors.Error as error:
            raise self._error(children=[error])

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref"]:
        return (
            root.Root.parser_rule().named("root")
            & part.Part.parser_rule()
            .zero_or_more()
            .convert(lambda parts: parts)
            .named("parts")
        ).convert(Ref)
