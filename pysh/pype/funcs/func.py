from dataclasses import dataclass, field
from pysh import core
from pysh.pype import lexer, parser
from pysh.pype.vals import args, builtins, scope, val
from pysh.pype.funcs import abstract_func


@dataclass(
    frozen=True,
    kw_only=True,
)
class Func(abstract_func.AbstractFunc):
    _name: str
    params: "params.Params" = field(default_factory=lambda: params.Params())
    body: "block.Block" = field(default_factory=lambda: block.Block())

    def name(self) -> str:
        return self._name

    def __call__(self, scope: scope.Scope, args: args.Args) -> val.Val:
        scope = self.params.bind(args, scope)
        result = self.body.eval(scope)
        return result.return_value if result.return_value is not None else builtins.none

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Func"]:
        return (
            "def"
            & core.parser.rules.Literal[parser.Parser](lexer.id)
            .token_value()
            .named("_name")
            & params.Params.parser_rule().named("params")
            & block.Block.ref().named("body")
        ).convert(Func)


from pysh.pype.exprs import params
from pysh.pype.statements import block
