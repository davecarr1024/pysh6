from abc import ABC, abstractmethod
from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Part(ABC):
    @abstractmethod
    def eval(self, scope: scope.Scope, val: val.Val) -> val.Val:
        ...

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Part"]:
        return call.Call.parser_rule() | member.Member.parser_rule()


from pysh.pype.exprs.ref.parts import call, member
