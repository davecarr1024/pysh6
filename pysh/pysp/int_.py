from dataclasses import dataclass
from pysh import core
from pysh.pysp import error, parser, val


@dataclass(frozen=True)
class Int(val.Val):
    value: int

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Int"]:
        def convert(token: core.tokens.Token) -> Int:
            try:
                return Int(int(token.value))
            except Exception as error_:
                raise error.Error(msg=f"failed to load int val: {error_}")

        return core.parser.rules.Literal[parser.Parser](
            core.lexer.Rule.load("int", r"\d+")
        ).convert(convert)
