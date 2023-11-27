from dataclasses import dataclass
from pysh import core
from pysh.pysp import parser, val


@dataclass(frozen=True)
class Int(val.Val):
    value: int

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Int"]:
        def convert(token: core.tokens.Token) -> Int:
            return cls._cls_try(lambda: Int(int(token.value)))

        return core.parser.rules.Literal[parser.Parser](
            core.lexer.Rule.load("int", r"\d+")
        ).convert(convert)
