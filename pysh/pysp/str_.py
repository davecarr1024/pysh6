from dataclasses import dataclass
from pysh import core
from pysh.pysp import error, parser, val


@dataclass(frozen=True)
class Str(val.Val):
    value: str

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Str"]:
        return (
            core.parser.rules.Literal[parser.Parser](
                core.lexer.Rule.load("str", '"(^")*"')
            )
            .token_value()
            .convert(lambda value: Str(value.strip('"')))
        )
