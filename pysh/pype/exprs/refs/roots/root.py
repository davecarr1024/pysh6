from abc import ABC, abstractmethod
from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Root(
    ABC,
    core.errors.Errorable["Root"],
):
    @abstractmethod
    def get(self, scope: scope.Scope) -> val.Val:
        ...

    @abstractmethod
    def set(self, scope: scope.Scope, val: val.Val) -> None:
        ...

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Root"]:
        return literal.Literal.parser_rule() | name.Name.parser_rule()

    @staticmethod
    def create(value: str | val.Val) -> "Root":
        match value:
            case str():
                return name.Name(value)
            case val.Val():
                return literal.Literal(value)


from pysh.pype.exprs.refs.roots import literal, name
