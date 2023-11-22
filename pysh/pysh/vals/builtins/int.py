from dataclasses import dataclass
from typing import Callable
from pysh import core
from pysh.pysh import parser
from . import class_, object_


@dataclass(frozen=True)
class Int(object_.Object["Int"]):
    value: int

    @property
    def type(self) -> class_.Class:
        return int_class

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Int"]:
        return (
            core.parser.rules.Literal[parser.Parser](
                core.lexer.Rule.load("int", r"\d+")
            )
            .token_value()
            .convert(lambda value: int_class.create(int(value)))
        )


int_class = class_.Class(Int)
int_: Callable[[int], Int] = int_class.create
