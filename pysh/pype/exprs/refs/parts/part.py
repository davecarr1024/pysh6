from abc import ABC, abstractmethod
from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import args
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Part(ABC):
    @abstractmethod
    def get(self, scope: scope.Scope, obj: val.Val) -> val.Val:
        ...

    @abstractmethod
    def set(self, scope: scope.Scope, obj: val.Val, val: val.Val) -> None:
        ...

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Part"]:
        return call.Call.parser_rule() | member.Member.parser_rule()

    @staticmethod
    def create(value: str | args.Args) -> "Part":
        match value:
            case str():
                return member.Member(value)
            case args.Args():
                return call.Call(value)


from pysh.pype.exprs.refs.parts import call, member
