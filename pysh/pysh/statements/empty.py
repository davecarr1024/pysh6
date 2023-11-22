from dataclasses import dataclass
from pysh import core
from pysh.pysh import parser, state

from pysh.pysh.statements import result, statement


@dataclass(frozen=True)
class Empty(statement.Statement):
    def _str_line(self) -> str:
        return ";"

    def eval(self, state: state.State) -> result.Result:
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Empty"]:
        return core.parser.rules.Literal[parser.Parser].load(";").no().convert(Empty)
