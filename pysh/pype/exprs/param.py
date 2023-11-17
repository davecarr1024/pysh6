from dataclasses import dataclass
from pysh import core
from pysh.pype import lexer, parser, vals


@dataclass(frozen=True)
class Param:
    name: str

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Param"]:
        return (
            core.parser.rules.Literal[parser.Parser](lexer.id)
            .token_value()
            .convert(Param)
        )
