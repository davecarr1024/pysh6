from dataclasses import dataclass
from pysh import core
from pysh.pysh import parser
from pysh.pysh.vals import val


@dataclass(frozen=True)
class Arg:
    val: "val.Val"

    def __str__(self) -> str:
        return str(self.val)

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Arg"]:
        return val.Val.parser_rule().convert(Arg)
