from dataclasses import dataclass
from pysh import core
from pysh.pysh import parser
from pysh.pysh.vals.classes import abstract_class
from pysh.pysh.vals import type, val


@dataclass(frozen=True)
class Int(val.Val):
    value: int

    @property
    def type(self) -> "type.Type":
        return int_class

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Int"]:
        return (
            core.parser.rules.Literal[parser.Parser](
                core.lexer.Rule.load("int", r"\d+")
            )
            .token_value()
            .convert(lambda value: Int(int(value)))
        )


int_class = abstract_class.AbstractClass("int")
