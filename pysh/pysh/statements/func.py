from dataclasses import dataclass
from typing import cast
from pysh import core
from pysh.pysh import lexer, parser, state
from pysh.pysh.vals import type, var
from pysh.pysh.vals.builtins import func_
from pysh.pysh.vals.funcs import func
from pysh.pysh.exprs import params, ref
from pysh.pysh.statements import block, result, statement


@dataclass(frozen=True)
class Func(statement.Statement):
    name: str
    return_type: ref.Ref
    params: params.Params
    body: block.Block

    def _str_line(self) -> str:
        return f"def {self.name}{self.params} -> {self.return_type}\n{self.body}"

    def eval(self, state: state.State) -> result.Result:
        if not isinstance(return_type := self.return_type.eval(state), type.Type):
            raise self._error(msg=f"invalid return type {return_type}")
        self._try(
            lambda: state.__setitem__(
                self.name,
                var.Var(
                    func_,
                    func.Func(
                        self.name,
                        cast(type.Type, return_type),
                        self.params.bind(state),
                        self.body,
                    ),
                ),
            ),
            "setting func val",
        )
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Func"]:
        return (
            "def"
            & lexer.id.named("name")
            & params.Params.parser_rule().named("params")
            & r"\-\>"
            & ref.Ref.ref().named("return_type")
            & block.Block.ref().named("body")
        ).convert(Func)
