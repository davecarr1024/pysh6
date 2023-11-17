from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.exprs import args
from pysh.pype.exprs.refs.parts import part
from pysh.pype.vals import scope, val


@dataclass(frozen=True)
class Call(part.Part):
    args: args.Args

    def __str__(self) -> str:
        return str(self.args)

    def get(self, scope: scope.Scope, val: val.Val) -> val.Val:
        return val(scope, self.args.eval(scope))

    def set(self, scope: scope.Scope, obj: val.Val, val: val.Val) -> None:
        raise core.errors.Error(msg=f"unable to set call {self}")

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Call"]:
        return args.Args.parser_rule().convert(Call)
