from dataclasses import dataclass, field
from typing import Sequence
from pysh import core
from pysh.pype import lexer, parser
from pysh.pype.vals import scope, val
from pysh.pype.vals.classes import class_
from pysh.pype.statements import statement


@dataclass(frozen=True)
class Class(statement.Statement):
    name: str
    body: Sequence["statement.Statement"] = field(
        default_factory=lambda: list[statement.Statement]()
    )

    def eval(self, scope_: scope.Scope) -> statement.Statement.Result:
        members = scope.Scope()
        for statement_ in self.body:
            statement_.eval(members)
        c = class_.Class(
            _name=self.name,
            members=members,
        )
        scope_[c.name()] = c
        return statement.Statement.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Class"]:
        return (
            "class"
            & core.parser.rules.Literal[parser.Parser](lexer.id)
            .token_value()
            .named("name")
            & "{"
            & statement.Statement.ref()
            .zero_or_more()
            .convert(lambda body: body)
            .named("body")
            & "}"
            & ";"
        ).convert(Class)
