from abc import ABC, abstractmethod
from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Root(ABC):
    @abstractmethod
    def get(self, scope: scope.Scope) -> val.Val:
        ...

    @abstractmethod
    def set(self, scope: scope.Scope, val: val.Val) -> None:
        ...

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Root"]:
        return literal.Literal.parser_rule() | name.Name.parser_rule()


from pysh.pype.exprs.ref.roots import literal, name
