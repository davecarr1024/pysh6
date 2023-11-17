from dataclasses import dataclass, field
from typing import Sequence
from pysh import core
from pysh.pype import lexer, parser
from pysh.pype.vals import scope
from pysh.pype.vals.classes import class_
from pysh.pype.statements import func, result, statement


@dataclass(frozen=True)
class Class(statement.Statement):
    name: str
    body: Sequence[func.Func] = field(default_factory=list)

    def eval(self, scope_: scope.Scope) -> result.Result:
        members = scope.Scope()
        for statement_ in self.body:
            statement_.eval(members)
        c = class_.Class(
            _name=self.name,
            members=members,
        )
        scope_[c.name()] = c
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Class"]:
        return (
            "class"
            & core.parser.rules.Literal[parser.Parser](lexer.id)
            .token_value()
            .named("name")
            & "{"
            & func.Func.ref()
            .convert(lambda func: func.as_bindable())
            .zero_or_more()
            .convert(lambda body: body)
            .named("body")
            & "}"
        ).convert(Class)
