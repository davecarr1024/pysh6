from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope
from pysh.pype.statements import result, statement


@dataclass(frozen=True)
class Empty(statement.Statement):
    def __str__(self) -> str:
        return ";"

    def eval(self, scope: scope.Scope) -> result.Result:
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Empty"]:
        return (
            core.parser.rules.Literal[parser.Parser]
            .load(";")
            .no()
            .convert(lambda: Empty())
        )
