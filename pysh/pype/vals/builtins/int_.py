from dataclasses import dataclass
from typing import cast
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope
from pysh.pype.vals.builtins import class_, value_object


@dataclass(frozen=True)
class Int(value_object.ValueObject[int]):
    @staticmethod
    def create(value: int) -> "Int":
        return cast(Int, int_class.create(value=value))

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Int"]:
        def convert(value: str) -> Int:
            try:
                return Int.create(int(value))
            except Exception as error:
                raise core.errors.Error(msg=f"failed to load int from {value}: {error}")

        return (
            core.parser.rules.Literal[parser.Parser](
                core.lexer.Rule.load("int", r"\d+")
            )
            .token_value()
            .convert(convert)
        )


int_class = class_.Class(
    _name="Int",
    _object_type=Int,
    members=scope.Scope(),
)
